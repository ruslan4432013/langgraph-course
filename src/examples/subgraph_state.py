from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict


class State(TypedDict):
    foo: str


# Subgraph

def subgraph_node_1(state: State):
    value = interrupt("Provide value:")
    return {"foo": state["foo"] + value}


subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")

subgraph = subgraph_builder.compile()

# Parent graph

builder = StateGraph(State)
builder.add_node("node_1", subgraph)
builder.add_edge(START, "node_1")

checkpointer = MemorySaver()
graph_checkpointer = builder.compile(checkpointer=checkpointer)
graph = builder.compile()

config = {"configurable": {"thread_id": "1"}}

result_1 = graph_checkpointer.invoke({"foo": ""}, config)

print(result_1)

parent_state = graph_checkpointer.get_state(config)

print(parent_state)

# This will be available only when the subgraph is interrupted.
# Once you resume the graph, you won't be able to access the subgraph state.
subgraph_state = graph_checkpointer.get_state(config, subgraphs=True).tasks[0].state

print(subgraph_state)

# resume the subgraph
result_2 = graph_checkpointer.invoke(Command(resume="bar"), config)

print(result_2)
