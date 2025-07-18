# Давайте создадим нашего агента
from langchain_deepseek import ChatDeepSeek

def multiply(a: int, b: int) -> int:
    """Умножить a и b.
    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a * b

# Это будет инструмент
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

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Системное сообщение
sys_msg = SystemMessage(content="Вы полезный ассистент, выполняющий арифметические операции над набором входных данных.")

# Узел
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Построитель графа
builder = StateGraph(MessagesState)

# Определяем узлы: они выполняют работу
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Определяем ребра: они определяют поток управления
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # Если последнее сообщение (результат) от ассистента - вызов инструмента -> tools_condition направляет к tools
    # Если последнее сообщение (результат) от ассистента - не вызов инструмента -> tools_condition направляет к END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(checkpointer=MemorySaver())
