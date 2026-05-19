import asyncio

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.client.settings import settings

llm = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    temperature=0.1,
    api_key=settings.PROXY_API_KEY.get_secret_value(),
    base_url="https://api.proxyapi.ru/anthropic"
)

client = MultiServerMCPClient(
    {
        "to-do-list": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
        }
    }
)


class State(MessagesState):
    pass


async def call_llm(state: State) -> State:
    # Получение всех списков дел
    blobs = await client.get_resources(server_name="to-do-list", uris=["to-do://lists"])
    task_lists = [blob.as_string() for blob in blobs]

    # Получение промпта
    prompt = await client.get_prompt(
        server_name="to-do-list",
        prompt_name="prompt_to_do_list",
        arguments={
            "names": task_lists[0],
        }
    )
    messages = prompt + state["messages"]
    response = await llm.ainvoke(messages)
    return {"messages": response}


@tool
async def get_tasks(name_list: str) -> str:
    """Просмотреть задачи всех списков через ресурс `to-do://tasks'"""
    blobs = await client.get_resources(server_name="to-do-list", uris=[f"to-do://tasks"])
    return [blob.as_string() for blob in blobs][0]


tools = asyncio.run(client.get_tools())
tools.append(get_tasks)
llm = llm.bind_tools(tools)
call_tools = ToolNode(tools=tools)

graph = StateGraph(State)

graph.add_node("model", call_llm)
graph.add_node("tools", call_tools)

graph.add_edge(START, "model")
graph.add_conditional_edges("model", tools_condition)
graph.add_edge("tools", "model")
graph.add_edge("model", END)

agent = graph.compile()

if __name__ == '__main__':
    result = asyncio.run(
        agent.ainvoke({"messages": "Пойду в магазин купить хлеб, молоко и яйца"})
    )
    print(result["messages"][-1].pretty_print())
    result = asyncio.run(
        agent.ainvoke({"messages": "Что нужно сделать в магазине, я забыл"})
    )
    print(result["messages"][-1].pretty_print())
