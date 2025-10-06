from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode

from src.components.llm_model import llm
from src.web_rag_application.tools.retrieve import retrieve


# Шаг 1: Сгенерировать AIMessage, который может содержать вызов инструмента для отправки.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState добавляет сообщения к состоянию вместо перезаписи
    return {"messages": [response]}


# Шаг 2: Выполнить получение (retrieval).
tool_node = ToolNode([retrieve])


# Шаг 3: Сгенерировать ответ, используя полученный контент.
def generate(state: MessagesState):
    """Generate answer."""
    # Получить сгенерированные ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Сформировать подсказку (prompt)
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
           or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Запуск
    response = llm.invoke(prompt)
    return {"messages": [response]}
