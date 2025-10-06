from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from src.components.llm_model import llm
from src.web_rag_application.tools.retrieve import retrieve

memory = MemorySaver()
agent_executor = create_react_agent(llm, [retrieve], checkpointer=memory)
