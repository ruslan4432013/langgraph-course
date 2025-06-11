from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_base='https://api.proxyapi.ru/deepseek',
    max_retries=2,
)


async def make_graph() -> CompiledGraph:
    graph = create_react_agent(llm, tools=[])
    return graph

if __name__ == '__main__':
    print(llm.invoke('Hello world'))