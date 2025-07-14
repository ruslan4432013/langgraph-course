from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState

from llm import llm


# Состояние
class State(MessagesState):
    summary: str


# Определяем логику вызова модели
def call_model(state: State, config: RunnableConfig):
    # Получаем сводку, если она существует
    summary = state.get("summary", "")

    # Если сводка есть, добавляем её
    if summary:
        # Добавляем сводку в системное сообщение
        system_message = f"Сводка предыдущего разговора: {summary}"
        # Добавляем сводку к новым сообщениям
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = llm.invoke(messages, config)
    return {"messages": response}


def summarize_conversation(state: State):
    # Сначала получаем существующую сводку
    summary = state.get("summary", "")

    # Создаём промт для суммаризации
    if summary:
        # Сводка уже существует
        summary_message = (
            f"Это сводка разговора на данный момент: {summary}\n\n"
            "Расширьте сводку, учитывая новые сообщения выше:"
        )
    else:
        summary_message = "Создайте сводку разговора выше:"

    # Добавляем промт в историю
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)

    # Удаляем все сообщения, кроме двух последних
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


# Определяем, завершать или суммаризировать разговор
def should_continue(state: State):
    """Возвращает следующий узел для выполнения."""
    messages = state["messages"]

    # Если сообщений больше шести, суммаризируем разговор
    if len(messages) > 6:
        return "summarize_conversation"

    # Иначе завершаем
    return END


# Определяем новый граф
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
# workflow.add_node("conversation_1", call_model)
workflow.add_node("summarize_conversation", summarize_conversation)

# Устанавливаем точку входа как "conversation"
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
# workflow.add_edge("conversation", "conversation_1")
workflow.add_edge("summarize_conversation", END)

# Компилируем
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
