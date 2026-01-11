from operator import add
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph


class State(TypedDict):
    messages: Annotated[list, add]


def node_a(state: State):
    return {"messages": ['A']}


def node_b(state: State):
    return {"messages": ['B']}


def node_c(state: State):
    return {"messages": ['C']}


workflow = StateGraph(State).add_sequence([node_a, node_b, node_c])
workflow.add_edge(START, "node_a")

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "2"}}
# print(graph.invoke({'messages': []}, config=config))


# for num, event in enumerate(graph.stream({"messages": []}, config, stream_mode="values")):
#     print("=" * 25 + f" Event {num} " + "=" * 25)
#     print(event)
#     print("=" * 59 + '\n')


for num, event in enumerate(graph.stream({"messages": []}, config, stream_mode="updates")):
    print("=" * 25 + f" Event {num} " + "=" * 25)
    print(event)
    print("=" * 59 + '\n')
