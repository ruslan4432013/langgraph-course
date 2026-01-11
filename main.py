from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph

from src.settings import settings

llm = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)


@tool
def add(x: int, y: int):
    """Add two numbers together."""
    return x + y


async def make_graph() -> CompiledStateGraph:
    graph = create_agent(llm, tools=[add])
    return graph


if __name__ == '__main__':
    print(llm.invoke('Hello world'))
