import operator
from typing import Annotated

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from lessons.module_4.assistant.analysts_workflow import Analyst

llm = ChatOpenAI(
    model='gpt-5',
    base_url="https://api.proxyapi.ru/openai/v1"
)


class InterviewState(MessagesState):
    max_num_turns: int  # Количество ходов беседы
    context: Annotated[list, operator.add]  # Исходные документы
    analyst: Analyst  # Аналитик, задающий вопросы
    interview: str  # Транскрипт интервью
    sections: list  # Финальный ключ, который мы дублируем во внешнем состоянии для Send() API


question_instructions = """
Ты аналитик, задача которого — провести интервью с экспертом, чтобы узнать о конкретной теме. 
Твоя цель — свести информацию к интересным и конкретным инсайтам, связанным с темой.
1. Интересно: инсайты, которые люди сочтут удивительными или неочевидными.
2. Конкретно: инсайты, которые избегают общих формулировок и включают конкретные примеры от эксперта.
Вот твоя тема фокуса и набор целей: {goals}
Начните с представления, используя имя, которое соответствует твоей персоне, а затем задай свой вопрос. 
Продолжай задавать вопросы, чтобы уточнять и углублять твое понимание темы. Когда ты будешь удовлетворен своим пониманием, заверши интервью фразой: "Большое спасибо за вашу помощь!"
Помните оставаться в образе на протяжении всего ответа, отражая персону и цели, которые вам предоставлены."""


def generate_question(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]
    system_message = question_instructions.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)
    return {"messages": [question]}


from pydantic import BaseModel, Field
from langchain_tavily import TavilySearch


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Запрос для поиска при извлечении. Только на английском языке")


search_instructions = SystemMessage(content=f"""Тебе будет дана беседа между аналитиком и экспертом. 
Твоя цель — сгенерировать хорошо структурированный запрос для использования при извлечении и/или веб-поиске, связанный с беседой. 
Сначала проанализируй всю беседу. Особое внимание удели последнему вопросу, заданному аналитиком. 
Преобразуй этот последний вопрос в хорошо структурированный запрос для веб-поиска.
""")

tavily_search = TavilySearch(max_results=20)


def search_web(state: InterviewState):
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state["messages"])
    search_docs = tavily_search.invoke(search_query.search_query)
    if not search_docs or not "results" in search_docs:
        return {"context": []}
    docs = search_docs["results"]
    formatted_search_docs = "\n\n---\n\n".join([f'\n{doc["content"]}\n' for doc in docs])
    return {"context": [formatted_search_docs]}


from langchain_community.document_loaders import WikipediaLoader


def search_wikipedia(state: InterviewState):
    structured_llm = llm.with_structured_output(SearchQuery)
    search_result = structured_llm.invoke([search_instructions] + state["messages"])
    search_docs = WikipediaLoader(query=search_result.search_query, load_max_docs=2).load()
    if not search_docs:
        return {"context": []}
    formatted_search_docs = "\n\n---\n\n".join([f'\n{doc.page_content}\n' for doc in search_docs])
    return {"context": [formatted_search_docs]}


answer_instructions = """Ты — эксперт, которого опрашивает аналитик. Ниже — область интересов аналитика: {goals}. 
Твоя цель — ответить на вопрос, заданный интервьюером. Для ответа на вопрос используй этот контекст: {context}
При ответе на вопросы следуй этим правилам:
1. Используй только информацию, приведённую в контексте.
2. Не вводи внешнюю информацию и не делай предположений, выходящих за рамки явно указанного в контексте.
3. Контекст содержит источники с указанием темы каждого отдельного документа.
4. Включай ссылки на эти источники рядом с любыми релевантными утверждениями. Например, для источника № 1 используй [1].
5. Перечисли свои источники в порядке внизу ответа. [1] Источник 1, [2] Источник 2 и т.д.
6. Если источник выглядит так: ' тогда просто укажи: [1] assistant/docs/llama3_1.pdf, page 7
   И при этом пропусти добавление скобок вокруг пути и префикса Document source в твоей ссылке.
"""


def generate_answer(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]
    system_message = answer_instructions.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)
    answer.name = "эксперт"
    return {"messages": [answer]}


from langchain_core.messages import AIMessage
from typing import Literal


def route_messages(state: InterviewState, name: str = "эксперт") -> Literal["save_interview", "ask_question"]:
    messages = state["messages"]
    max_num_turns = state.get("max_num_turns", 2)
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == name])
    if num_responses >= max_num_turns:
        return "save_interview"
    last_question = messages[-2]
    if "Большое спасибо за вашу помощь!" in last_question.content:
        return "save_interview"
    return "ask_question"


from langchain_core.messages import get_buffer_string


def save_interview(state: InterviewState):
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}


section_writer_instructions = """Ты — эксперт-технический писатель. 
Твоя задача — создать короткий, легко усваиваемый раздел отчёта на основе набора исходных документов-источников.
1. Проанализируй содержимое исходных документов:
   - Имя каждого исходного документа указано в начале документа с тегом 
Источники
[1] Название ссылки или документа

[2] Название ссылки или документа

7. Объединяй источники. Например, это неверно: [3] https://ai.meta.com/blog/meta-llama-3-1/ [4] https://ai.meta.com/blog/meta-llama-3-1/ — не должно быть дублирующихся источников. 
Должно быть просто: [3] https://ai.meta.com/blog/meta-llama-3-1/

8. Финальная проверка:

Убедись, что отчет следует требуемой структуре
Не добавляй вступления перед заголовком отчета
Проверь, что все руководства соблюдены
"""

from langchain_core.messages import HumanMessage


def write_section(state: InterviewState):
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]
    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke(
        [SystemMessage(content=system_message)] +
        [HumanMessage(content=f"Используй этот источник: {context}")]
    )
    return {"sections": [section.content]}


from langgraph.graph import StateGraph
from langgraph.constants import START, END
from langgraph.checkpoint.memory import MemorySaver

interview_builder = StateGraph(InterviewState)
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_wikipedia", search_wikipedia)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_wikipedia")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_wikipedia", "answer_question")
interview_builder.add_conditional_edges("answer_question", route_messages)
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

memory = MemorySaver()
interview_graph = interview_builder.compile(checkpointer=memory).with_config(run_name="Проведение интервью")

if __name__ == "__main__":
    topic = "пользе применения LangGraph фреймворка в компании"
    analyst = Analyst(
        affiliation="Лаборатория LangGraph AI", name="Игорь Лебедев",
        role="Аналитик по архитектуре и взаимодействию мультиагентной платформы LangGraph",
        description="Фокус на архитектурные принципы LangGraph..."
    )

    messages = [HumanMessage(f"Итак, вы сказали, что пишете статью о {topic}?")]
    thread = {"configurable": {"thread_id": "1"}}
    interview = interview_graph.invoke({"analyst": analyst, "messages": messages, "max_num_turns": 2}, thread)
    print(interview["sections"][0])
