from langgraph.graph.state import StateGraph, START
from typing_extensions import TypedDict


class State(TypedDict):
    foo: str


# Subgraph

def subgraph_node_1(state: State):
    return {"foo": "hi! " + state["foo"]}


subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

builder = StateGraph(State)
builder.add_node("node_1", subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"foo": "foo"})
    print(result)
