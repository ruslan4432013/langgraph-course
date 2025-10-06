from langgraph.checkpoint.memory import MemorySaver

from src.web_rag_application.web_rag_application import graph_builder

memory = MemorySaver()
graph_with_memory = graph_builder.compile(checkpointer=memory)
