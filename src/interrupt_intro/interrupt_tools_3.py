import sqlite3
from typing import TypedDict, Optional, Literal

from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


# =============================================================================
# ПРИМЕР 3: Interrupts в Tools
# =============================================================================

@tool
def send_email_tool(to: str, subject: str, body: str):
    """Отправляет email получателю (с подтверждением)"""
    # Приостанавливаем перед отправкой
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "Одобрить отправку этого email?",
    })

    if response.get("action") == "approve":
        # Resume value может переопределить входные параметры
        final_to = response.get("to", to)
        final_subject = response.get("subject", subject)
        final_body = response.get("body", body)

        # Симуляция отправки email
        print(f"📧 Email отправлен:")
        print(f"   Кому: {final_to}")
        print(f"   Тема: {final_subject}")
        print(f"   Текст: {final_body}")

        return f"Email успешно отправлен на {final_to}"

    return "Email отменен пользователем"


class AgentState(TypedDict):
    """Состояние для агента с tools"""
    messages: list


def agent_node(state: AgentState):
    """Узел агента (без LLM для простоты примера)"""
    # Вместо реального LLM, симулируем вызов tool
    print("\n🤖 Агент решает отправить email...")

    # Вызываем tool напрямую (в реальности это делал бы LLM)
    result = send_email_tool.invoke({
        "to": "alice@example.com",
        "subject": "Важное совещание",
        "body": "Приглашаем вас на совещание завтра в 10:00"
    })

    return {"messages": state["messages"] + [{"role": "tool", "content": result}]}


def create_tool_graph():
    """Создает граф с tool interrupts"""
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_edge(START, "agent")
    builder.add_edge("agent", END)

    checkpointer = SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))
    return builder.compile(checkpointer=checkpointer)


def demo_tool_interrupts():
    """Демонстрация interrupts в tools"""
    print("\n" + "=" * 70)
    print("ПРИМЕР 3: Interrupts в Tools")
    print("=" * 70)

    graph = create_tool_graph()
    config = {"configurable": {"thread_id": "tool-demo"}}

    print("\n📍 Запуск агента...")
    result = graph.invoke(
        {"messages": [{"role": "user", "content": "Отправь email Alice"}]},
        config=config,
    )

    print(f"\n⏸️  Tool приостановлен для подтверждения!")
    interrupt_data = result["__interrupt__"][0].value
    print(f"Email кому: {interrupt_data['to']}")
    print(f"Тема: {interrupt_data['subject']}")

    # Возобновляем с одобрением и измененной темой
    print(f"\n▶️  Одобряем с измененной темой...")
    final_result = graph.invoke(
        Command(resume={
            "action": "approve",
            "subject": "СРОЧНО: Важное совещание"  # Меняем тему
        }),
        config=config,
    )

    print(f"✅ Результат: {final_result['messages'][-1]['content']}")

demo_tool_interrupts()