import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


# =============================================================================
# ПРИМЕР 5: Множественные прерывания в одной ноде
# =============================================================================

class MultiInterruptState(TypedDict):
    """Состояние для множественных прерываний"""
    name: str
    age: int
    city: str


def collect_user_info_node(state: MultiInterruptState):
    """Узел, собирающий информацию через несколько interrupts"""
    print("📝 Собираем информацию о пользователе...")

    # Важно: порядок interrupt вызовов должен быть одинаковым!
    name = interrupt("Как вас зовут?")
    print(f"   Получено имя: {name}")

    age = interrupt("Сколько вам лет?")
    print(f"   Получен возраст: {age}")

    city = interrupt("В каком городе вы живете?")
    print(f"   Получен город: {city}")

    return {
        "name": name,
        "age": age,
        "city": city
    }


def create_multi_interrupt_graph():
    """Создает граф с множественными interrupts"""
    builder = StateGraph(MultiInterruptState)
    builder.add_node("collect_info", collect_user_info_node)
    builder.add_edge(START, "collect_info")
    builder.add_edge("collect_info", END)

    checkpointer = SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))
    return builder.compile(checkpointer=checkpointer)


def demo_multiple_interrupts():
    """Демонстрация множественных interrupts"""
    print("\n" + "=" * 70)
    print("ПРИМЕР 5: Множественные Interrupts в одной ноде")
    print("=" * 70)

    graph = create_multi_interrupt_graph()
    config = {"configurable": {"thread_id": "multi-interrupt-demo"}}

    # Первое прерывание - имя
    print("\n📍 Запуск сбора информации...")
    result1 = graph.invoke({"name": "", "age": 0, "city": ""}, config=config)
    print(f"\n⏸️  Прерывание 1: {result1['__interrupt__'][0].value}")

    # Отвечаем на первый вопрос
    print("▶️  Отвечаем: 'Алексей'")
    result2 = graph.invoke(Command(resume="Алексей"), config=config)
    print(f"\n⏸️  Прерывание 2: {result2['__interrupt__'][0].value}")

    # Отвечаем на второй вопрос
    print("▶️  Отвечаем: 28")
    result3 = graph.invoke(Command(resume=28), config=config)
    print(f"\n⏸️  Прерывание 3: {result3['__interrupt__'][0].value}")

    # Отвечаем на третий вопрос
    print("▶️  Отвечаем: 'Москва'")
    final_result = graph.invoke(Command(resume="Москва"), config=config)

    print(f"\n✅ Вся информация собрана:")
    print(f"   Имя: {final_result['name']}")
    print(f"   Возраст: {final_result['age']}")
    print(f"   Город: {final_result['city']}")


demo_multiple_interrupts()
