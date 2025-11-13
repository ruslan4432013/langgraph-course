from langchain_core.messages import SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from src.settings import settings


def multiply(a: int, b: int) -> int:
    """Умножить a и b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a * b


# Это будет инструментом
def add(a: int, b: int) -> int:
    """Сложить a и b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a + b


def divide(a: int, b: int) -> float:
    """Разделить a на b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a / b


tools = [add, multiply, divide]

llm = ChatDeepSeek(
    model='deepseek/deepseek-chat-v3.1',
    temperature=0.1,
    max_retries=2,
    api_base="https://api.proxyapi.ru/openrouter/v1",  # Необходимо, для работы модели через ProxyApi
    api_key=settings.API_KEY,
)

llm_with_tools = llm.bind_tools(tools)

# Системное сообщение
sys_msg = SystemMessage(content="Вы полезный помощник, выполняющий арифметические операции над набором входных данных.")


# Узел
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Построитель графа
builder = StateGraph(MessagesState)

# Определение узлов: они выполняют работу
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Определение ребер: они определяют поток управления
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # Если последнее сообщение (результат) от assistant - вызов инструмента -> tools_condition ведет к tools
    # Если последнее сообщение (результат) от assistant - не вызов инструмента -> tools_condition ведет к END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(interrupt_before=["assistant"], checkpointer=memory)
