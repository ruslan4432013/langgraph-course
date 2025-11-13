from operator import add
from pprint import pprint
from typing import Annotated, Any

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    foo: int
#
def node_1(state: State):
    print("---Node 1---")
    return {"foo": state['foo'] + 1}
#
# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
#
# # Add
graph = builder.compile()

# View
print(graph.invoke({"foo" : 1}))

# class State(TypedDict):
#     foo: int
#
# def node_1(state):
#     print("---Node 1---")
#     return {"foo": state['foo'] + 1}
#
# def node_2(state):
#     print("---Node 2---")
#     return {"foo": state['foo'] + 1}
#
# def node_3(state):
#     print("---Node 3---")
#     return {"foo": state['foo'] + 1}
#
# # Построение графа
# builder = StateGraph(State)
# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)
#
# # Логика
# builder.add_edge(START, "node_1")
# builder.add_edge("node_1", "node_2")
# builder.add_edge("node_1", "node_3")
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)
#
# # Добавление
# graph = builder.compile()
#
# # Просмотр
# from langgraph.errors import InvalidUpdateError
#
# try:
#     graph.invoke({"foo" : 1})
# except InvalidUpdateError as e:
#     print(f"InvalidUpdateError occurred: {e}")


# from operator import add
# from typing import Annotated
#
#
# class State(TypedDict):
#     foo: Annotated[list[int], add]
#
# def node_1(state):
#     print("---Node 1---")
#     return {"foo": [state['foo'][0] + 1]}
# #
# # # Построение графа
# builder = StateGraph(State)
# builder.add_node("node_1", node_1)
# #
# # # Логика
# builder.add_edge(START, "node_1")
# builder.add_edge("node_1", END)
# #
# # # Добавление
# graph = builder.compile()

# print(graph.invoke({"foo" : [1]}))

# def safe_reducer(a, b):
#     print(f"safe_reducer({a}, {b})")
#     if b is None:
#         return [0]
#     return a + b
#
# class State(TypedDict):
#     foo: Annotated[list[int], safe_reducer]
#
# def node_1(state):
#     print("---Node 1---")
#     return {"foo": [state['foo'][-1] + 1]}
#
# def node_2(state):
#     print("---Node 2---")
#     return {"foo": [state['foo'][-1] + 1]}
#
# def node_3(state):
#     print("---Node 3---")
#     return {"foo": [state['foo'][-1] + 1]}
#
# # Построение графа
# builder = StateGraph(State)
# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)
#
# # Логика
# builder.add_edge(START, "node_1")
# builder.add_edge("node_1", "node_2")
# builder.add_edge("node_1", "node_3")
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)
#
# # Добавление
# graph = builder.compile()
# #
# # print(graph.invoke({"foo" : [1]}))
# #
# try:
#     print(graph.invoke({"foo" : None}))
# except TypeError as e:
#     print(f"TypeError occurred: {e}")


from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

# # Начальное состояние
# initial_messages = [
#     AIMessage(content="Привет! Чем могу помочь?", name="Model"),
#     HumanMessage(content="Я ищу информацию по морской биологии.", name="Lance")
# ]
# #
# # # Новое сообщение для добавления
# new_message = AIMessage(content="Конечно, могу помочь. Что именно вас интересует?", name="Model")
# #
# # # Тестируем
# pprint(add_messages(initial_messages, new_message))

# # Начальное состояние
# initial_messages = [
#     AIMessage(content="Привет! Чем могу помочь?", name="Model", id="1"),
#     HumanMessage(content="Я ищу информацию по морской биологии.", name="Лэнс", id="2")
# ]
#
# # Новое сообщение для добавления
# new_message = HumanMessage(
#     content="Меня интересуют киты, в частности",
#     name="Лэнс",
#     id="2"
# )
# # Тест
# pprint(add_messages(initial_messages, new_message))

from langchain_core.messages import RemoveMessage
#
# # Список сообщений
# messages: list[BaseMessage] = [AIMessage("Hi.", name="Bot", id="1")]
# messages.append(HumanMessage("Hi.", name="Lance", id="2"))
# messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
# messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))
#
# # Выделяем сообщения для удаления
# delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
# print(delete_messages)
#
# pprint(add_messages(messages, delete_messages))



