from typing import Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import operator
from typing import Annotated

class State(TypedDict):
    # Функция-редуктор operator.add делает это состояние только для добавления:
    state: str

class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f"Добавляем {self._value} к {state['state']}")
        return {"state": [self._value]}

### Пример 1
# # Добавляем узлы
# builder = StateGraph(State)
#
# # Инициализируем каждый узел с node_secret
# builder.add_node("a", ReturnNodeValue("Узел A"))
# builder.add_node("b", ReturnNodeValue("Узел B"))
# builder.add_node("c", ReturnNodeValue("Узел C"))
# builder.add_node("d", ReturnNodeValue("Узел D"))
#
# # Поток
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("b", "c")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
#
# graph = builder.compile()
#
# print(graph.invoke({"state": []}))

### Пример 2
# builder = StateGraph(State)
#
# # Инициализируем каждый узел с node_secret
# builder.add_node("a", ReturnNodeValue("Узел A"))
# builder.add_node("b", ReturnNodeValue("Узел B"))
# builder.add_node("c", ReturnNodeValue("Узел C"))
# builder.add_node("d", ReturnNodeValue("Узел D"))
#
# # Поток
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "d")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
#
# graph = builder.compile()
#
# from langgraph.errors import InvalidUpdateError
#
# try:
#     print(graph.invoke({"state": []}))
# except InvalidUpdateError as e:
#     print(f"Произошла ошибка: {e}")


### Пример 3
# class State(TypedDict):
#     # Функция-редуктор operator.add делает это состояние только для добавления:
#     state: Annotated[list, operator.add]
#
# # Добавляем узлы
# builder = StateGraph(State)
#
# # Инициализируем каждый узел с node_secret
# builder.add_node("a", ReturnNodeValue("Узел A"))
# builder.add_node("b", ReturnNodeValue("Узел B"))
# builder.add_node("c", ReturnNodeValue("Узел C"))
# builder.add_node("d", ReturnNodeValue("Узел D"))
#
# # Поток
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "d")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
#
# graph = builder.compile()
#
# print(graph.invoke({"state": []}))


### Пример 4
class State(TypedDict):
    # Функция-редуктор operator.add делает это состояние только для добавления:
    state: Annotated[list, operator.add]

builder = StateGraph(State)
# Инициализация каждого узла с node_secret
builder.add_node("a", ReturnNodeValue("Узел A"))
builder.add_node("b", ReturnNodeValue("Узел B"))
builder.add_node("b2", ReturnNodeValue("Узел B2"))
builder.add_node("c", ReturnNodeValue("Узел C"))
builder.add_node("d", ReturnNodeValue("Узел D"))

# Поток выполнения
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge(["b2", "c"], "d")
builder.add_edge("d", END)

graph = builder.compile()
# print(graph.invoke({"state": []}))

### Пример 5
# def sorting_reducer(left, right):
#     """Объединяет и сортирует значения в списке"""
#     if not isinstance(left, list):
#         left = [left]
#     if not isinstance(right, list):
#         right = [right]
#     return sorted(left + right, reverse=False)
#
# class State(TypedDict):
#     # sorting_reducer отсортирует значения в состоянии
#     state: Annotated[list, sorting_reducer]
#
# # Добавляем узлы
# builder = StateGraph(State)
#
# # Инициализируем каждый узел с node_secret
# builder.add_node("a", ReturnNodeValue("Узел A"))
# builder.add_node("b", ReturnNodeValue("Узел B"))
# builder.add_node("b2", ReturnNodeValue("Узел B2"))
# builder.add_node("c", ReturnNodeValue("Узел C"))
# builder.add_node("d", ReturnNodeValue("Узел D"))
#
# # Поток выполнения
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "b2")
# builder.add_edge(["b2", "c"], "d")
# builder.add_edge("d", END)
#
# graph = builder.compile()
# print(graph.invoke({"state": []}))