import sqlite3
from typing import TypedDict, Optional, Literal

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


# =============================================================================
# ПРИМЕР 1: Простое Approval Workflow
# =============================================================================
class ApprovalState(TypedDict):
    """Состояние для workflow с подтверждением"""
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]


def approval_node(state: ApprovalState) -> Command[Literal["proceed", "cancel"]]:
    """Узел, который запрашивает подтверждение действия"""
    # Приостанавливаем выполнение и показываем детали действия
    decision = interrupt({
        "question": "Одобрить это действие?",
        "details": state["action_details"],
    })

    # Маршрутизация на основе ответа
    return Command(goto="proceed" if decision else "cancel")


def proceed_node(state: ApprovalState):
    """Узел для одобренного действия"""
    print(f"✅ Действие одобрено: {state['action_details']}")
    return {"status": "approved"}


def cancel_node(state: ApprovalState):
    """Узел для отмененного действия"""
    print(f"❌ Действие отклонено: {state['action_details']}")
    return {"status": "rejected"}


def create_approval_graph():
    """Создает граф для approval workflow"""
    builder = StateGraph(ApprovalState)
    builder.add_node("approval", approval_node)
    builder.add_node("proceed", proceed_node)
    builder.add_node("cancel", cancel_node)

    builder.add_edge(START, "approval")
    builder.add_edge("proceed", END)
    builder.add_edge("cancel", END)

    checkpointer = SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))
    return builder.compile(checkpointer=checkpointer)


def demo_approval_workflow():
    """Демонстрация approval workflow"""
    print("\n" + "=" * 70)
    print("ПРИМЕР 1: Approval Workflow")
    print("=" * 70)

    graph = create_approval_graph()
    config = {"configurable": {"thread_id": "approval-demo-1"}}

    # Первый запуск - граф остановится на interrupt
    print("\n📍 Запуск графа...")
    result = graph.invoke(
        {"action_details": "Перевести $500 на счет клиента", "status": "pending"},
        config=config,
    )

    # Проверяем payload из interrupt
    print(f"\n⏸️  Граф приостановлен!")
    print(f"Interrupt payload: {result['__interrupt__']}")

    # Продолжаем с одобрением
    print("\n▶️  Возобновляем с одобрением (resume=True)...")
    final_result = graph.invoke(Command(resume=True), config=config)
    print(f"Финальный статус: {final_result['status']}")

    # # Запуск с отклонением
    # print("\n---\n📍 Новый запуск с отклонением...")
    # config2 = {"configurable": {"thread_id": "approval-demo-2"}}
    # result2 = graph.invoke(
    #     {"action_details": "Удалить базу данных", "status": "pending"},
    #     config=config2,
    # )
    #
    # print(f"⏸️  Граф приостановлен!")
    # print(f"▶️  Возобновляем с отклонением (resume=False)...")
    # final_result2 = graph.invoke(Command(resume=False), config=config2)
    # print(f"Финальный статус: {final_result2['status']}")


demo_approval_workflow()