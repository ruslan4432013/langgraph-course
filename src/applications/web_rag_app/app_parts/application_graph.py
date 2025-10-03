from langgraph.graph import START, StateGraph

from src.applications.web_rag_app.app_parts.app_nodes import generate, retrieve, analyze_query
from src.applications.web_rag_app.app_parts.app_states import State

graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate])
graph_builder.add_edge(START, "analyze_query")
graph = graph_builder.compile()
