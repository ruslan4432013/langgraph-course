# Системное сообщение
from langchain_core.messages import SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


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
    model='deepseek-chat',
    temperature=0.1,
    max_retries=2,
    api_base="https://api.proxyapi.ru/deepseek"
)

llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="Вы полезный ассистент, которому поручено выполнять арифметические операции над набором входных данных.")

# no-op узел, который должен быть прерван
def human_feedback(state: MessagesState):
    pass

# Узел ассистента
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Построение графа
builder = StateGraph(MessagesState)

# Определение узлов: они выполняют работу
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("human_feedback", human_feedback)

# Определение ребер: они определяют поток управления
builder.add_edge(START, "human_feedback")
builder.add_edge("human_feedback", "assistant")
builder.add_conditional_edges(
    "assistant",
    # Если последнее сообщение (результат) от ассистента - вызов инструмента -> tools_condition направляет к tools
    # Если последнее сообщение (результат) от ассистента - не вызов инструмента -> tools_condition направляет к END
    tools_condition,
)
builder.add_edge("tools", "human_feedback")

memory = MemorySaver()
graph = builder.compile(interrupt_before=["human_feedback"], checkpointer=memory)
