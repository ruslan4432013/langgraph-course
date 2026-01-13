import sqlite3
from typing import Optional, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


# =============================================================================
# ПРИМЕР 4: Validation Loop
# =============================================================================

class FormState(TypedDict):
    """Состояние формы"""
    age: Optional[int]
    attempts: int


def get_age_node(state: FormState):
    """Узел для получения и валидации возраста"""
    prompt = "Введите ваш возраст:"
    attempts = state.get("attempts", 0)

    while True:
        attempts += 1
        answer = interrupt(prompt)

        # Валидация
        if isinstance(answer, int) and answer > 0 and answer < 150:
            print(f"✅ Валидный возраст получен после {attempts} попыток")
            return {"age": answer, "attempts": attempts}
        else:
            prompt = f"⚠️  '{answer}' - некорректный возраст. Введите положительное число (1-150):"


def create_validation_graph():
    """Создает граф с валидацией"""
    builder = StateGraph(FormState)
    builder.add_node("collect_age", get_age_node)
    builder.add_edge(START, "collect_age")
    builder.add_edge("collect_age", END)

    checkpointer = SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))
    return builder.compile(checkpointer=checkpointer)


def demo_validation():
    """Демонстрация validation loop"""
    print("\n" + "=" * 70)
    print("ПРИМЕР 4: Validation Loop")
    print("=" * 70)

    graph = create_validation_graph()
    config = {"configurable": {"thread_id": "validation-demo"}}

    # Первая попытка
    print("\n📍 Запуск формы...")
    result1 = graph.invoke({"age": None, "attempts": 0}, config=config)
    print(f"⏸️  {result1['__interrupt__'][0].value}")

    # Некорректный ввод
    print("\n▶️  Вводим некорректные данные: 'тридцать'")
    result2 = graph.invoke(Command(resume="тридцать"), config=config)
    print(f"⏸️  {result2['__interrupt__'][0].value}")

    # Еще одна некорректная попытка
    print("\n▶️  Вводим отрицательное число: -5")
    result3 = graph.invoke(Command(resume=-5), config=config)
    print(f"⏸️  {result3['__interrupt__'][0].value}")

    # Корректный ввод
    print("\n▶️  Вводим корректное значение: 30")
    final_result = graph.invoke(Command(resume=30), config=config)
    print(f"✅ Возраст сохранен: {final_result['age']}")
    print(f"   Всего попыток: {final_result['attempts']}")


demo_validation()