import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


# =============================================================================
# ПРИМЕР 2: Review and Edit State
# =============================================================================
class ReviewState(TypedDict):
    """Состояние для проверки и редактирования"""
    generated_text: str


def review_node(state: ReviewState):
    """Узел для проверки и редактирования текста"""
    # Показываем текущий контент для проверки
    edited_content = interrupt({
        "instruction": "Проверьте и отредактируйте этот контент",
        "content": state["generated_text"],
    })

    return {"generated_text": edited_content}


def create_review_graph():
    """Создает граф для review workflow"""
    builder = StateGraph(ReviewState)
    builder.add_node("review", review_node)
    builder.add_edge(START, "review")
    builder.add_edge("review", END)

    checkpointer = SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))
    return builder.compile(checkpointer=checkpointer)


def demo_review_and_edit():
    """Демонстрация review and edit workflow"""
    print("\n" + "=" * 70)
    print("ПРИМЕР 2: Review and Edit State")
    print("=" * 70)

    graph = create_review_graph()
    config = {"configurable": {"thread_id": "review-demo"}}

    initial_text = "Это первоначальный черновик текста с опечатками."

    print(f"\n📍 Запуск с текстом: '{initial_text}'")
    result = graph.invoke({"generated_text": initial_text}, config=config)

    print(f"\n⏸️  Граф приостановлен для проверки!")
    print(f"Текущий текст: {result['__interrupt__'][0].value['content']}")

    # Возобновляем с отредактированным текстом
    edited_text = "Это исправленный финальный текст без ошибок."
    print(f"\n▶️  Возобновляем с отредактированным текстом...")
    final_result = graph.invoke(Command(resume=edited_text), config=config)

    print(f"✅ Финальный текст: {final_result['generated_text']}")


demo_review_and_edit()