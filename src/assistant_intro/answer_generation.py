import logging
import operator
from typing import Annotated, Literal

from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, get_buffer_string
from langchain_tavily import TavilySearch
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from pydantic import BaseModel, Field

from src.assistant_intro.analysts_workflow import Analyst
from src.assistant_intro.llm import llm
from src.settings import settings

logger = logging.getLogger(__name__)


class InterviewState(MessagesState):
    max_num_turns: int  # Количество ходов беседы
    context: Annotated[list, operator.add]  # Исходные документы
    analyst: Analyst  # Аналитик, задающий вопросы
    interview: str  # Транскрипт интервью
    sections: list  # Финальный ключ


class SearchQuery(BaseModel):
    search_query: str = Field(description="Запрос для поиска. Только на английском языке")


# === Промпты ===
QUESTION_INSTRUCTIONS = """Ты аналитик, задача которого — провести интервью с экспертом, чтобы узнать о конкретной теме. 
Твоя цель — свести информацию к интересным и конкретным инсайтам, связанным с темой.
1. Интересно: инсайты, которые люди сочтут удивительными или неочевидными.
2. Конкретно: инсайты, которые избегают общих формулировок и включают конкретные примеры от эксперта.

Вот твоя тема фокуса и набор целей: {goals}

Начни с представления, используя имя, которое соответствует твоей персоне, а затем задай свой вопрос. 
Продолжай задавать вопросы, чтобы уточнять и углублять твое понимание темы. 
Когда ты будешь удовлетворён своим пониманием, заверши интервью фразой: "Большое спасибо за вашу помощь!"
Оставайся в образе на протяжении всего ответа, отражая персону и цели, которые тебе предоставлены."""

SEARCH_INSTRUCTIONS = """Тебе будет дана беседа между аналитиком и экспертом. 
Твоя цель — сгенерировать хорошо структурированный запрос для веб-поиска на английском языке.
Проанализируй беседу и особенно последний вопрос аналитика. 
Преобразуй его в лаконичный поисковый запрос (3-7 слов)."""

ANSWER_INSTRUCTIONS = """Ты — эксперт, которого опрашивает аналитик.
Область интересов аналитика: {goals}

Для ответа на вопрос используй этот контекст:
{context}

Правила:
1. Используй только информацию из контекста.
2. Не делай предположений, выходящих за рамки контекста.
3. Включай ссылки на источники рядом с релевантными утверждениями: [1], [2] и т.д.
4. Перечисли источники в конце ответа.
5. Если контекст не содержит релевантной информации, честно скажи об этом."""

SECTION_WRITER_INSTRUCTIONS = """Ты — эксперт-технический писатель. 
Создай короткий, структурированный раздел отчёта на основе интервью.

Фокус раздела: {focus}

Требования:
1. Начни сразу с заголовка раздела (##)
2. Используй маркированные списки для ключевых пунктов
3. Включи 1-2 конкретных примера или инсайта
4. Объём: 150-300 слов
5. Укажи источники в конце раздела
6. Не дублируй источники"""

# === Инструменты поиска ===
tavily_search = TavilySearch(max_results=5, tavily_api_key=settings.TAVILY_API_KEY)


def _extract_search_query(state: InterviewState) -> str | None:
    """Извлечь поисковый запрос из состояния."""
    structured_llm = llm.with_structured_output(SearchQuery)
    try:
        result = structured_llm.invoke(
            [SystemMessage(content=SEARCH_INSTRUCTIONS)] + state["messages"]
        )
        return result.search_query if result else None
    except Exception as e:
        logger.warning(f"Ошибка генерации поискового запроса: {e}")
        return None


def search_web(state: InterviewState) -> dict:
    """Поиск через Tavily."""
    query = _extract_search_query(state)
    if not query:
        return {"context": []}

    try:
        search_docs = tavily_search.invoke(query)
        if not search_docs or "results" not in search_docs:
            return {"context": []}

        docs = search_docs["results"][:5]  # Ограничиваем количество
        formatted = "\n\n---\n\n".join(
            f"[Источник: {doc.get('url', 'N/A')}]\n{doc['content']}"
            for doc in docs if doc.get("content")
        )
        return {"context": [formatted] if formatted else []}
    except Exception as e:
        logger.error(f"Ошибка веб-поиска: {e}")
        return {"context": []}


def search_wikipedia(state: InterviewState) -> dict:
    """Поиск в Wikipedia."""
    query = _extract_search_query(state)
    if not query:
        return {"context": []}

    try:
        docs = WikipediaLoader(query=query, load_max_docs=2).load()
        if not docs:
            return {"context": []}

        formatted = "\n\n---\n\n".join(
            f"[Wikipedia: {doc.metadata.get('title', 'N/A')}]\n{doc.page_content[:2000]}"
            for doc in docs
        )
        return {"context": [formatted] if formatted else []}
    except Exception as e:
        logger.warning(f"Ошибка поиска Wikipedia: {e}")
        return {"context": []}


# === Узлы графа ===
def generate_question(state: InterviewState) -> dict:
    """Генерация вопроса аналитиком."""
    analyst = state["analyst"]
    system_message = QUESTION_INSTRUCTIONS.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + state["messages"])
    return {"messages": [question]}


def generate_answer(state: InterviewState) -> dict:
    """Генерация ответа экспертом."""
    analyst = state["analyst"]
    context = state.get("context", [])

    # Объединяем контекст из всех источников
    combined_context = "\n\n".join(context) if context else "Контекст не найден."

    system_message = ANSWER_INSTRUCTIONS.format(
        goals=analyst.persona,
        context=combined_context
    )
    answer = llm.invoke([SystemMessage(content=system_message)] + state["messages"])
    answer.name = "эксперт"
    return {"messages": [answer]}


def route_messages(state: InterviewState) -> Literal["save_interview", "ask_question"]:
    """Роутинг: продолжить интервью или завершить."""
    messages = state["messages"]
    max_turns = state.get("max_num_turns", 2)

    # Считаем ответы эксперта
    expert_responses = sum(
        1 for m in messages
        if isinstance(m, AIMessage) and getattr(m, "name", None) == "эксперт"
    )

    if expert_responses >= max_turns:
        return "save_interview"

    # Проверяем фразу завершения в последнем вопросе
    if len(messages) >= 2:
        last_question = messages[-2]
        if hasattr(last_question, "content") and "Большое спасибо за вашу помощь!" in last_question.content:
            return "save_interview"

    return "ask_question"


def save_interview(state: InterviewState) -> dict:
    """Сохранение транскрипта интервью."""
    interview = get_buffer_string(state["messages"])
    return {"interview": interview}


def write_section(state: InterviewState) -> dict:
    """Написание раздела отчёта."""
    analyst = state["analyst"]
    interview = state.get("interview", "")
    context = state.get("context", [])

    system_message = SECTION_WRITER_INSTRUCTIONS.format(focus=analyst.description)
    combined_input = f"Интервью:\n{interview}\n\nИсточники:\n{chr(10).join(context)}"

    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=combined_input)
    ])
    return {"sections": [section.content]}


# === Построение графа ===
def build_interview_graph():
    """Создание и компиляция графа интервью."""
    builder = StateGraph(InterviewState)

    # Добавление узлов
    builder.add_node("ask_question", generate_question)
    builder.add_node("search_web", search_web)
    builder.add_node("search_wikipedia", search_wikipedia)
    builder.add_node("answer_question", generate_answer)
    builder.add_node("save_interview", save_interview)
    builder.add_node("write_section", write_section)

    # Построение потока
    builder.add_edge(START, "ask_question")
    builder.add_edge("ask_question", "search_web")
    builder.add_edge("ask_question", "search_wikipedia")
    builder.add_edge("search_web", "answer_question")
    builder.add_edge("search_wikipedia", "answer_question")
    builder.add_conditional_edges("answer_question", route_messages)
    builder.add_edge("save_interview", "write_section")
    builder.add_edge("write_section", END)

    return builder.compile().with_config(run_name="Проведение интервью")


interview_graph = build_interview_graph()

if __name__ == "__main__":
    topic = "пользе применения LangGraph фреймворка в компании"
    analyst = Analyst(
        affiliation="Лаборатория LangGraph AI",
        name="Игорь Лебедев",
        role="Аналитик по архитектуре мультиагентной платформы LangGraph",
        description="Фокус на архитектурные принципы LangGraph и преимущества для бизнеса"
    )

    messages = [HumanMessage(content=f"Итак, вы сказали, что пишете статью о {topic}?")]
    thread = {"configurable": {"thread_id": "1"}}

    result = interview_graph.invoke(
        {"analyst": analyst, "messages": messages, "max_num_turns": 2},
        thread
    )
    print(result["sections"][0])
