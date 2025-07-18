from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import NodeInterrupt
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    input: str

def step_1(state: State) -> State:
    print("---Шаг 1---")
    return state

def step_2(state: State) -> State:
    # Опционально вызываем NodeInterrupt, если длина ввода больше 5 символов
    if len(state['input']) > 5:
        print("---Шаг 2 Прерван---")
        raise NodeInterrupt(f"Получен ввод длиннее 5 символов: {state['input']}")
    print("---Шаг 2---")
    return state

def step_3(state: State) -> State:
    print("---Шаг 3---")
    return state

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

# Настраиваем память
memory = MemorySaver()

# Компилируем граф с памятью
graph = builder.compile(checkpointer=memory)
graph_studio = builder.compile()
