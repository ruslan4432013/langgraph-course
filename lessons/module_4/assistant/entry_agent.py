import operator
from typing import List, Annotated

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send
from typing_extensions import TypedDict

from lessons.module_4.assistant.analysts_workflow import create_analysts, human_feedback, Analyst
from lessons.module_4.assistant.answer_generation import interview_builder
from lessons.module_4.assistant.model import llm


class ResearchGraphState(TypedDict):
    topic: str  # Тема исследования
    max_analysts: int  # Количество аналитиков
    human_analyst_feedback: str  # Обратная связь от человека-аналитика
    analysts: List[Analyst]  # Аналитики, задающие вопросы
    sections: Annotated[list, operator.add]  # Секции отчета (объединяются оператором add)
    introduction: str  # Введение для итогового отчета
    content: str  # Основное содержание итогового отчета
    conclusion: str  # Заключение для итогового отчета
    final_report: str  # Итоговый отчет


def initiate_all_interviews(state: ResearchGraphState):
    """Это шаг «map», где мы запускаем каждый суб-граф интервью через API Send."""
    # Проверяем, есть ли обратная связь от человека-аналитика
    human_analyst_feedback = state.get('human_analyst_feedback')
    if human_analyst_feedback:
        # Возвращаемся к create_analysts
        return "create_analysts"
    # Иначе запускаем интервью параллельно через Send() API
    else:
        topic = state["topic"]
        return [
            Send("conduct_interview", {"analyst": analyst, "messages": [HumanMessage(
                content=f"Вы сказали, что пишете статью на тему {topic}?"
            )]})
            for analyst in state["analysts"]
        ]


report_writer_instructions = """Вы — технический писатель, готовящий отчет по общей теме: {topic}
У вас есть команда аналитиков. Каждый аналитик сделал две вещи:
1. Провёл интервью с экспертом по конкретной подтеме.
2. Оформил свои выводы в меморандуме.

Ваша задача:
1. Вам будет предоставлена коллекция меморандумов от ваших аналитиков.
2. Тщательно проанализируйте инсайты из каждого меморандума.
3. Сведите их в чёткое общее резюме, связывающее центральные идеи всех меморандумов.
4. Суммируйте ключевые моменты каждого меморандума в единое связное повествование.

Форматирование отчета:
1. Используйте форматирование markdown.
2. Не включайте вступительных слов перед отчетом.
3. Не используйте подзаголовки.
4. Начните отчёт с единого заголовка: ## Выводы
5. Не упоминайте имена аналитиков в отчёте.
6. Сохраняйте любые цитирования в меморандумах — они будут помечены в скобках, например [1] или [2].
7. Создайте финальный, консолидированный список источников и добавьте его в раздел с заголовком `## Источники`.
8. Перечислите источники в порядке и не дублируйте их.

[1] Источник 1
[2] Источник 2

Вот меморандумы от ваших аналитиков, на основе которых нужно создать отчёт: {context}"""


def write_report(state: ResearchGraphState):
    # Полный набор секций
    sections = state["sections"]
    topic = state["topic"]

    # Объединяем все секции в одну строку
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Суммируем секции в итоговый отчет
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)
    report = llm.invoke([SystemMessage(content=system_message)] + [
        HumanMessage(content=f"Напишите отчёт на основе этих меморандумов.")])
    return {"content": report.content}


intro_conclusion_instructions = """Вы — технический писатель, завершающий отчёт по теме {topic}
Вам будут предоставлены все секции отчёта. Ваша задача — написать короткое и убедительное введение или заключение.
Пользователь укажет, писать введение или заключение.
Не включайте вступительных слов для любой секции.
Целевая длина — около 100 слов, ёмко представляя (для введения) или подытоживая (для заключения) все секции отчёта.
Используйте форматирование markdown.
Для введения создайте выразительный заголовок с использованием заголовка уровня #.
Для введения используйте заголовок раздела ## Введение.
Для заключения используйте заголовок раздела ## Заключение.

Вот секции, на которые нужно опереться при написании: {formatted_str_sections}"""


def write_introduction(state: ResearchGraphState):
    # Полный набор секций
    sections = state["sections"]
    topic = state["topic"]

    # Объединяем все секции в одну строку
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Суммируем секции для написания введения
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = llm.invoke([instructions] + [HumanMessage(content=f"Напишите введение к отчёту")])
    return {"introduction": intro.content}


def write_conclusion(state: ResearchGraphState):
    # Полный набор секций
    sections = state["sections"]
    topic = state["topic"]

    # Объединяем все секции в одну строку
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Суммируем секции для написания заключения
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    conclusion = llm.invoke([instructions] + [HumanMessage(content=f"Напишите заключение к отчёту")])
    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
    """Это шаг «reduce», где мы собираем все секции, объединяем их и формируем введение/заключение."""
    # Сохраняем полное содержание итогового отчёта
    content = state["content"]
    if content.startswith("## Выводы"):
        content = content.strip("## Выводы")
    if "## Источники" in content:
        try:
            content, sources = content.split("\n## Источники\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Источники\n" + sources
    return {"final_report": final_report}


# Добавляем узлы и связи
builder = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_builder.compile())
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

# Логика графа
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", initiate_all_interviews, ["create_analysts", "conduct_interview"])
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
builder.add_edge("finalize_report", END)

# Компиляция
memory = MemorySaver()
analyst_graph = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)
graph = builder.compile(interrupt_before=['human_feedback'])

if __name__ == "__main__":
    # Зададим открытый вопрос про LangGraph.
    # Входные данные
    max_analysts = 3
    topic = "Какая польза применения LangGraph фреймворка в компании"
    thread = {"configurable": {"thread_id": "1"}}

    # Запускаем граф до первой точки остановки
    for event in analyst_graph.stream({"topic": topic, "max_analysts": max_analysts}, thread, stream_mode="values"):
        analysts = event.get('analysts', '')
        if analysts:
            for analyst in analysts:
                print(f"Имя: {analyst.name}")
                print(f"Аффилиация: {analyst.affiliation}")
                print(f"Роль: {analyst.role}")
                print(f"Описание: {analyst.description}")
                print("-" * 50)

    # Теперь обновляем состояние так, как если бы мы были узлом human_feedback
    analyst_graph.update_state(thread,
                               {"human_analyst_feedback": "Добавьте CEO нативного стартапа в области генеративного ИИ"},
                               as_node="human_feedback")

    # Проверяем следующие события
    for event in analyst_graph.stream(None, thread, stream_mode="values"):
        analysts = event.get('analysts', '')
        if analysts:
            for analyst in analysts:
                print(f"Имя: {analyst.name}")
                print(f"Аффилиация: {analyst.affiliation}")
                print(f"Роль: {analyst.role}")
                print(f"Описание: {analyst.description}")
                print("-" * 50)

    # Подтверждаем, что всё устраивает
    analyst_graph.update_state(thread, {"human_analyst_feedback": None}, as_node="human_feedback")

    # Продолжаем
    for event in analyst_graph.stream(None, thread, stream_mode="updates"):
        print("--Узел--")
        node_name = next(iter(event.keys()))
        print(node_name)

    final_state = analyst_graph.get_state(thread)
    report = final_state.values.get('final_report')
    print(report)
