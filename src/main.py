from typing_extensions import TypedDict
from typing import Literal
import random
from langgraph.graph import StateGraph, START, END


def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"


#########################################  TypedDict  ##############################################################
class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy", "sad"]


def node_1(state):
    print("---Node 1---")
    return {"name": state['name'] + " is ... "}


def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}


def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}


builder = StateGraph(TypedDictState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

print(graph.invoke({"name": "Lance"}))

#########################################  Dataclass  ##############################################################
# from dataclasses import dataclass
#
# @dataclass
# class DataclassState:
#     name: str
#     mood: Literal["happy", "sad"]
#
# def node_1(state):
#     print("---Node 1---")
#     return {"name": state.name + " is ... "}
#
# def node_2(state):
#     print("---Node 2---")
#     print(state.name)
#     return {"mood": "happy"}
#
# def node_3(state):
#     print("---Node 3---")
#     print(state.name)
#     return {"mood": "sad"}
#
# builder = StateGraph(DataclassState)
# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)
#
# builder.add_edge(START, "node_1")
# builder.add_conditional_edges("node_1", decide_mood)
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)
#
# graph = builder.compile()
#
# result = graph.invoke(DataclassState(name="Lance", mood="sad"))
#
# print(result)
#
# try:
#     print(result.name)
# except Exception as e:
#     print('Конечный результат все равно будет в виде словаря')

#########################################  Pydantic  ##############################################################
#
# from pydantic import BaseModel, field_validator, ValidationError
#
#
# class PydanticState(BaseModel):
#     name: str
#     mood: str  # "happy" или "sad"
#
#     @field_validator('mood')
#     @classmethod
#     def validate_mood(cls, value):
#         if value not in ["happy", "sad"]:
#             raise ValueError("Each mood must be either 'happy' or 'sad'")
#         return value
#
#
# try:
#     state = PydanticState(name="John Doe", mood="mad")
# except ValidationError as e:
#     print("Validation Error:", e)
#
#
# def node_1(state: PydanticState):
#     print("---Node 1---")
#     return {"name": state.name + " is ... "}
#
#
# def node_2(state: PydanticState):
#     print("---Node 2---")
#     print(state.name)
#     return {"mood": "happy"}
#
#
# def node_3(state: PydanticState):
#     print("---Node 3---")
#     print(state.name)
#     return {"mood": "sad!"}
#
#
# builder = StateGraph(PydanticState)
# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)
#
# builder.add_edge(START, "node_1")
# builder.add_conditional_edges("node_1", decide_mood)
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)
#
# graph = builder.compile()
#
# result = graph.invoke(PydanticState(name="Lance", mood="sad"))
#
# try:
#     error_result = graph.invoke(PydanticState(name="Lance", mood="Здесь не валидное значение"))
# except ValidationError as e:
#     print("Validation Error:", e)
#
# print(result)
#
# try:
#     print(result.name)
# except Exception as e:
#     print('Конечный результат все равно будет в виде словаря')
