from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.graph.state import CompiledStateGraph

from src.settings import settings

llm = ChatDeepSeek(
    model='deepseek/deepseek-chat-v3.1',
    temperature=0.1,
    max_retries=2,
    api_base="https://api.proxyapi.ru/openrouter/v1",  # Необходимо, для работы модели через ProxyApi
    api_key=settings.API_KEY,
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
