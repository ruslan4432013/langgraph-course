################################### Пример 1: Приватное состояние ######################################################
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# Схемы состояния
class OverallState(TypedDict):
    foo: int


class PrivateState(TypedDict):
    baz: int


# Узлы графа
def node_1(state: OverallState) -> PrivateState:
    print("---Node 1---")
    return {"baz": state['foo'] + 1}


def node_2(state: PrivateState) -> OverallState:
    print("---Node 2---")
    return {"foo": state['baz'] + 1}


# Построение графа
builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Логика связей
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Компиляция графа
graph = builder.compile()

# Вызов графа
print(graph.invoke({"foo": 1}))

################################### Пример 2: Фильтрация входных и выходных данных #####################################
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END
#
# # Схемы состояния
# class InputState(TypedDict):
#     question: str
#
# class OutputState(TypedDict):
#     answer: str
#
#
# class OverallState(TypedDict):
#     question: str
#     answer: str
#     notes: str
#
# # Узлы графа
# def thinking_node(state: InputState) -> OverallState:
#     return {"answer": "bye", "notes": "... his name is Lance"}
#
# def answer_node(state: OverallState) -> OutputState:
#     return {"answer": "bye Lance"}
#
# # Построение графа
# graph = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
# graph.add_node("thinking_node", thinking_node)
# graph.add_node("answer_node", answer_node)
#
# # Логика связей
# graph.add_edge(START, "thinking_node")
# graph.add_edge("thinking_node", "answer_node")
# graph.add_edge("answer_node", END)
#
# # Компиляция графа
# graph = graph.compile()
#
# # Вызов графа
# print(graph.invoke({"question": "hi"}))
