# Инструмент веб-поиска
from typing import Literal

from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from lessons.module_4.assistant.analysts_workflow import Analyst
from lessons.module_4.assistant.expert import InterviewState, SearchQuery, generate_question
from lessons.module_4.assistant.model import llm

tavily_search = TavilySearch(max_results=3)

# Инструмент поиска по Википедии

# Теперь создаём узлы для поиска в вебе и в Википедии.
# Также создадим узел для ответа на вопросы аналитика.
# Наконец, создадим узлы для сохранения полного интервью и для написания резюме ("section") интервью.

from langchain_core.messages import get_buffer_string, SystemMessage, HumanMessage, AIMessage

# Инструкции для написания запроса поиска
search_instructions = SystemMessage(content=f"""Тебе будет дана беседа между аналитиком и экспертом. 
Твоя цель — сгенерировать хорошо структурированный запрос для использования при извлечении и/или веб-поиске, связанный с беседой. 
Сначала проанализируй всю беседу. Особое внимание удели последнему вопросу, заданному аналитиком. 
Преобразуй этот последний вопрос в хорошо структурированный запрос для веб-поиска, используя русский язык.
""")


def search_web(state: InterviewState):
    """Извлечь документы через веб-поиск"""
    # Подготовка запросa к поиску
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state['messages'])
    # Поиск
    search_docs = tavily_search.invoke(search_query.search_query)
    if not search_docs or not 'results' in search_docs:
        return {"context": []}
    
    docs = search_docs['results']
    # Форматирование
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'\n{doc["content"]}\n'
            for doc in docs
        ]
    )
    return {"context": [formatted_search_docs]}


def search_wikipedia(state: InterviewState):
    """Извлечь документы из Википедии"""
    # Подготовка запроса к поиску
    structured_llm = llm.with_structured_output(SearchQuery)
    search_result = structured_llm.invoke([search_instructions] + state['messages'])
    # Поиск
    search_docs = WikipediaLoader(query=search_result.search_query, load_max_docs=2, lang='ru').load()
    if not search_docs:
        return {"context": []}

    # Форматирование
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'\n{doc.page_content}\n'
            for doc in search_docs
        ]
    )
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
    """Узел для ответа на вопрос"""
    # Получить состояние
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    # Сформировать системное сообщение для ответа
    system_message = answer_instructions.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)

    # Назвать сообщение как от эксперта
    answer.name = "эксперт"

    # Добавить его в состояние
    return {"messages": [answer]}


def save_interview(state: InterviewState):
    """Сохранить интервью"""
    # Получить сообщения
    messages = state["messages"]
    # Конвертировать интервью в строку
    interview = get_buffer_string(messages)
    # Сохранить в ключ interviews
    return {"interview": interview}


def route_messages(state: InterviewState, name: str = "эксперт") -> Literal['save_interview', 'ask_question']:
    """Маршрутизировать между вопросом и ответом"""
    # Получить сообщения
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)

    # Проверить количество ответов эксперта
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == name])

    # Завершить, если эксперт ответил больше, чем максимально разрешено
    if num_responses >= max_num_turns:
        return 'save_interview'

    # Этот маршрутизатор запускается после каждой пары вопрос-ответ
    # Получить последний заданный вопрос, чтобы проверить, сигнализирует ли он о завершении обсуждения
    last_question = messages[-2]
    if "Большое спасибо за твою помощь" in last_question.content:
        return 'save_interview'

    return "ask_question"


section_writer_instructions = """Ты — эксперт-технический писатель. Твоя задача — создать короткий, легко усваиваемый раздел отчёта на основе набора исходных документов-источников.
1. Проанализируй содержимое исходных документов:
   - Имя каждого исходного документа указано в начале документа с тегом 
Источники
[1] Название ссылки или документа

[2] Название ссылки или документа

7. Объединяй источники. Например, это неверно: [3] https://ai.meta.com/blog/meta-llama-3-1/ [4] https://ai.meta.com/blog/meta-llama-3-1/ — не должно быть дублирующихся источников. Должно быть просто: [3] https://ai.meta.com/blog/meta-llama-3-1/

8. Финальная проверка:

Убедись, что отчет следует требуемой структуре
Не добавляй вступления перед заголовком отчета
Проверь, что все руководства соблюдены

"""


def write_section(state: InterviewState):
    """Узел для ответа на вопрос"""
    # Получить состояние
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]
    # Написать раздел, используя либо собранные документы из интервью (context), либо само интервью (interview)
    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke(
        [SystemMessage(content=system_message)]
        + [HumanMessage(content=f"Используй этот источник для написания раздела: {context}")]
    )
    # Добавить его в состояние
    return {"sections": [section.content]}


# Добавить узлы и ребра
interview_builder = StateGraph(InterviewState)
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_wikipedia", search_wikipedia)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

# Поток
interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_wikipedia")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_wikipedia", "answer_question")
interview_builder.add_conditional_edges("answer_question", route_messages)
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

# Интервью
memory = MemorySaver()
interview_graph = interview_builder.compile(checkpointer=memory).with_config(run_name="Проведение интервью")
graph = interview_builder.compile().with_config(run_name="Проведение интервью")

# Выбрать одного аналитика
# Здесь мы запускаем интервью, передавая индекс статьи llama3.1, которая связана с нашей темой.
if __name__ == "__main__":
    topic = "Какая польза применения LangGraph фреймворка в компании"
    analyst = Analyst(affiliation='Лаборатория LangGraph AI', name='Игорь Лебедев',
                      role='Аналитик по архитектуре и взаимодействию мультиагентной платформы LangGraph',
                      description='Фокус на архитектурные принципы LangGraph, протоколы обмена между агентами, координацию задач, управление контекстом, безопасность и отказоустойчивость мультиагентной среды.')
    messages = [HumanMessage(f"Итак, вы сказали, что пишете статью о {topic}?")]
    thread = {"configurable": {"thread_id": "1"}}
    interview = interview_graph.invoke({"analyst": analyst, "messages": messages, "max_num_turns": 2}, thread)
    print(interview['sections'][0])
