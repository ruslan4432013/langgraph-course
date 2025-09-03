import operator


from typing import List, Annotated

from langchain\_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send
from typing\_extensions import TypedDict

from lessons.module\_4.assistant.analysts\_workflow import create\_analysts, human\_feedback, Analyst
from lessons.module\_4.assistant.answer\_generation import interview\_builder
from lessons.module\_4.assistant.model import llm

class ResearchGraphState(TypedDict):
topic: str  # Тема исследования
max\_analysts: int  # Количество аналитиков
human\_analyst\_feedback: str  # Обратная связь от человека-аналитика
analysts: List\[Analyst]  # Аналитики, задающие вопросы
sections: Annotated\[list, operator.add]  # Секции отчета (объединяются оператором add)
introduction: str  # Введение для итогового отчета
content: str  # Основное содержание итогового отчета
conclusion: str  # Заключение для итогового отчета
final_report: str  # Итоговый отчет

def initiate\_all\_interviews(state: ResearchGraphState):
"""Это шаг «map», где мы запускаем каждый суб-граф интервью через API Send."""
\# Проверяем, есть ли обратная связь от человека-аналитика
human\_analyst\_feedback = state.get('human\_analyst\_feedback')
if human\_analyst\_feedback:
\# Возвращаемся к create\_analysts
return "create\_analysts"
\# Иначе запускаем интервью параллельно через Send() API
else:
topic = state\["topic"]
return \[
Send("conduct\_interview", {"analyst": analyst, "messages": \[HumanMessage(
content=f"Вы сказали, что пишете статью на тему {topic}?"
)]})
for analyst in state\["analysts"]
]

report\_writer\_instructions = """Вы — технический писатель, готовящий отчет по общей теме: {topic}
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
6. Сохраняйте любые цитирования в меморандумах — они будут помечены в скобках, например \[1] или \[2].
7. Создайте финальный, консолидированный список источников и добавьте его в раздел с заголовком `## Источники`.
8. Перечислите источники в порядке и не дублируйте их.

\[1] Источник 1
\[2] Источник 2

Вот меморандумы от ваших аналитиков, на основе которых нужно создать отчёт: {context}"""

def write\_report(state: ResearchGraphState):
\# Полный набор секций
sections = state\["sections"]
topic = state\["topic"]


# Объединяем все секции в одну строку
formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

# Суммируем секции в итоговый отчет
system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)
report = llm.invoke([SystemMessage(content=system_message)] + [
    HumanMessage(content=f"Напишите отчёт на основе этих меморандумов.")])
return {"content": report.content}


intro\_conclusion\_instructions = """Вы — технический писатель, завершающий отчёт по теме {topic}
Вам будут предоставлены все секции отчёта. Ваша задача — написать короткое и убедительное введение или заключение.
Пользователь укажет, писать введение или заключение.
Не включайте вступительных слов для любой секции.
Целевая длина — около 100 слов, ёмко представляя (для введения) или подытоживая (для заключения) все секции отчёта.
Используйте форматирование markdown.
Для введения создайте выразительный заголовок с использованием заголовка уровня #.
Для введения используйте заголовок раздела ## Введение.
Для заключения используйте заголовок раздела ## Заключение.

Вот секции, на которые нужно опереться при написании: {formatted\_str\_sections}"""

def write\_introduction(state: ResearchGraphState):
\# Полный набор секций
sections = state\["sections"]
topic = state\["topic"]


# Объединяем все секции в одну строку
formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

# Суммируем секции для написания введения
instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
intro = llm.invoke([instructions] + [HumanMessage(content=f"Напишите введение к отчёту")])
return {"introduction": intro.content}


def write\_conclusion(state: ResearchGraphState):
# Полный набор секций
sections = state\["sections"]
topic = state\["topic"]


# Объединяем все секции в одну строку
formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

# Суммируем секции для написания заключения
instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
conclusion = llm.invoke([instructions] + [HumanMessage(content=f"Напишите заключение к отчёту")])
return {"conclusion": conclusion.content}

def finalize\_report(state: ResearchGraphState):
"""Это шаг «reduce», где мы собираем все секции, объединяем их и формируем введение/заключение."""
\# Сохраняем полное содержание итогового отчёта
content = state\["content"]
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
builder.add\_node("create\_analysts", create\_analysts)
builder.add\_node("human\_feedback", human\_feedback)
builder.add\_node("conduct\_interview", interview\_builder.compile())
builder.add\_node("write\_report", write\_report)
builder.add\_node("write\_introduction", write\_introduction)
builder.add\_node("write\_conclusion", write\_conclusion)
builder.add\_node("finalize\_report", finalize\_report)

# Логика графа

builder.add\_edge(START, "create\_analysts")
builder.add\_edge("create\_analysts", "human\_feedback")
builder.add\_conditional\_edges("human\_feedback", initiate\_all\_interviews, \["create\_analysts", "conduct\_interview"])
builder.add\_edge("conduct\_interview", "write\_report")
builder.add\_edge("conduct\_interview", "write\_introduction")
builder.add\_edge("conduct\_interview", "write\_conclusion")
builder.add\_edge(\["write\_conclusion", "write\_report", "write\_introduction"], "finalize\_report")
builder.add\_edge("finalize\_report", END)

# Компиляция

memory = MemorySaver()
analyst\_graph = builder.compile(interrupt\_before=\['human\_feedback'], checkpointer=memory)
graph = builder.compile(interrupt\_before=\['human\_feedback'])

if __name__ == "__main__":
# Зададим открытый вопрос про LangGraph.
# Входные данные
max_analysts = 3
topic = "Какая польза применения LangGraph фреймворка в компании"
thread = {"configurable": {"thread\_id": "1"}}


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
    if analysts := event.get('analysts', ''):
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