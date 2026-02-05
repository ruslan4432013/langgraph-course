from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    foo: str


# Subgraph

def subgraph_node_1(state: State):
    return {"foo": state["foo"] + "bar"}


subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# Parent graph

builder = StateGraph(State)
builder.add_node("node_1", subgraph)
builder.add_edge(START, "node_1")

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    result = graph.invoke({"foo": "foo"}, config={'thread_id': 1})
    print(result)
