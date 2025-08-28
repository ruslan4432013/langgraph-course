from typing import List, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from lessons.module_4.assistant.model import llm


class Analyst(BaseModel):
    affiliation: str = Field(
        description="Основная аффилиация аналитика.",
    )
    name: str = Field(
        description="Имя аналитика."
    )
    role: str = Field(
        description="Роль аналитика в контексте темы.",
    )
    description: str = Field(
        description="Описание фокуса аналитика, его забот и мотивов.",
    )

    @property
    def persona(self) -> str:
        return f"Имя: {self.name}\nРоль: {self.role}\nАффилиация: {self.affiliation}\nОписание: {self.description}\n"


class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(
        description="Полный список аналитиков с их ролями и аффилиациями.",
    )


class GenerateAnalystsState(TypedDict):
    topic: str  # Тема исследования
    max_analysts: int  # Количество аналитиков
    human_analyst_feedback: str  # Обратная связь от человека
    analysts: List[Analyst]  # Аналитики, задающие вопросы


analyst_instructions = """Тебе поручено создать набор персон аналитиков ИИ. Тщательно следуйте этим инструкциям:
1. Сначала ознакомьтесь с темой исследования: {topic}
2. Изучите любые редакционные замечания, которые при необходимости были предоставлены для руководства при создании аналитиков: {human_analyst_feedback}
3. Определите наиболее интересные темы на основе документов и/или обратной связи выше.
4. Выберите топ {max_analysts} тем.
5. Назначьте по одному аналитику на каждую тему.
"""


def create_analysts(state: GenerateAnalystsState):
    """Создать аналитиков"""
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    # Обеспечить структурированный вывод
    structured_llm = llm.with_structured_output(Perspectives)

    # Системное сообщение
    system_message = analyst_instructions.format(topic=topic, human_analyst_feedback=human_analyst_feedback,
                                                 max_analysts=max_analysts)

    # Сгенерировать запрос
    analysts = structured_llm.invoke(
        [SystemMessage(content=system_message)] + [HumanMessage(content="Сгенерируй набор аналитиков")])

    # Записать список аналитиков в состояние
    return {"analysts": analysts.analysts}


def human_feedback(state: GenerateAnalystsState):
    """Узел без операции, который должен прерываться"""
    pass


def should_continue(state: GenerateAnalystsState) -> Literal['create_analysts', END]:
    """Вернуть следующий узел для выполнения"""
    # Проверить, есть ли обратная связь от человека
    human_analyst_feedback = state.get('human_analyst_feedback', None)
    if human_analyst_feedback:
        return "create_analysts"
    # В противном случае завершить
    return END


# Добавить узлы и ребра
builder = StateGraph(GenerateAnalystsState)
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue, ["create_analysts", END])

# Компиляция
memory = MemorySaver()
app = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)
graph = builder.compile(interrupt_before=['human_feedback'])

if __name__ == "__main__":
    # Ввод
    max_analysts = 3
    topic = "Преимущества внедрения LangGraph как мультиагентного фреймворка"
    thread: RunnableConfig = {"configurable": {"thread_id": "1"}}

    # Запустить граф до первой точки остановки
    for event in app.stream({"topic": topic, "max_analysts": max_analysts}, thread, stream_mode="values"):
        print(event)
        # Просмотр результатов
        analysts: list[Analyst] = event.get('analysts', [])
        if analysts:
            for analyst in analysts:
                print(f"Имя: {analyst.name}")
                print(f"Аффилиация: {analyst.affiliation}")
                print(f"Роль: {analyst.role}")
                print(f"Описание: {analyst.description}")
                print("-" * 50)
        print(analysts)
    # Получить состояние и посмотреть следующий узел
    state = app.get_state(thread)
    print(f'{state.next=}')

    # Теперь мы обновляем состояние так, как если бы мы были узлом human_feedback
    app.update_state(thread, {
        "human_analyst_feedback": "Добавить кого-то из стартапа, чтобы добавить предпринимательскую перспективу"},
                     as_node="human_feedback")

    # Продолжить выполнение графа
    for event in app.stream(None, thread, stream_mode="values"):
        # Просмотр результатов
        analysts: list[Analyst] = event.get('analysts', [])
        if analysts:
            for analyst in analysts:
                print(f"Имя: {analyst.name}")
                print(f"Аффилиация: {analyst.affiliation}")
                print(f"Роль: {analyst.role}")
                print(f"Описание: {analyst.description}")
                print("-" * 50)

    # Если мы удовлетворены, то просто не предоставляем дополнительную обратную связь
    further_feedback = None
    app.update_state(thread, {"human_analyst_feedback": further_feedback}, as_node="human_feedback")

    # Продолжить выполнение графа до завершения
    for event in app.stream(None, thread, stream_mode="updates"):
        print("--Узел--")
        node_name = next(iter(event.keys()))
        print(node_name)
        final_state = app.get_state(thread)
        analysts = final_state.values.get('analysts')
        print(final_state.next)
        for analyst in analysts:
            print(f"Имя: {analyst.name}")
            print(f"Аффилиация: {analyst.affiliation}")
            print(f"Роль: {analyst.role}")
            print(f"Описание: {analyst.description}")
            print("-" * 50)
