from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from src.components.llm_model import llm
from src.web_rag_application.tools.retrieve import retrieve

memory = MemorySaver()
agent_executor = create_agent(llm, [retrieve], checkpointer=memory)
