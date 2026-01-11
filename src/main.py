from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from src.settings import settings


# Арифметические инструменты
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

     Args:
         a: first int
         b: second int
     """
    return a * b


def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


tools = [add, multiply, divide]

# Инициализация модели
llm = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="Ты помощник для выполнения арифметических операций.")


def assistant(state: MessagesState) -> MessagesState:
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


tools_node = ToolNode(tools=tools)

builder = StateGraph(MessagesState)

# Добавление узлов
builder.add_node("assistant", assistant)
builder.add_node("tools", tools_node)

# Определение рёбер
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # Если последнее сообщение - вызов инструмента → переход к tools
    # Если не вызов инструмента → переход к END
    tools_condition
)
builder.add_edge("tools", "assistant")  # Ключевое ребро цикла

memory = MemorySaver()
react_graph = builder.compile(checkpointer=memory)
react_graph_cli = builder.compile()

if __name__ == '__main__':
    config = {"configurable": {"thread_id": "1"}}

    messages_1 = [HumanMessage(content="Сложи 3 и 4")]
    result = react_graph.invoke({"messages": messages_1}, config=config)
    for m in result['messages']:
        m.pretty_print()

    messages_2 = [HumanMessage(content="Умножь это на 2.")]
    messages = react_graph.invoke({"messages": messages_2}, config=config)

    for m in messages['messages']:
        m.pretty_print()
