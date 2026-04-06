import asyncio

from langchain_core.tools import tool
from langchain_mcp_adapters.callbacks import Callbacks
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from mcp.types import ElicitResult

from src.settings import settings


# --- Callbacks для MCP ---

async def on_log(params, context):
    """Обработчик логов от MCP-сервера."""
    print(f"[{params.level}] ({context.server_name}) {params.data}")


async def on_elicitation(mcp_context, params, context):
    """Обработчик запросов эликитации от сервера."""
    print(f"\n--- Запрос от сервера ({context.server_name}) ---")
    print(f"Сообщение: {params.message}")

    # Если сервер запрашивает только подтверждение (без схемы данных)
    if not params.requestedSchema or not params.requestedSchema.get("properties"):
        answer = input("Подтвердить? (y/n): ").strip().lower()
        if answer == "y":
            return ElicitResult(action="accept", content={})
        else:
            return ElicitResult(action="decline")

    # Если сервер запрашивает данные — собираем по схеме
    content = {}
    for field_name, field_schema in params.requestedSchema.get("properties", {}).items():
        title = field_schema.get("title", field_name)
        description = field_schema.get("description", "")

        if "enum" in field_schema:
            options = field_schema["enum"]
            print(f"{title} ({description}). Варианты: {', '.join(options)}")
            value = input(f"  {title}: ").strip()
        else:
            value = input(f"  {title} ({description}): ").strip()

        # Приведение типов
        if field_schema.get("type") == "integer":
            value = int(value)
        elif field_schema.get("type") == "boolean":
            value = value.lower() in ("true", "1", "yes", "y")

        content[field_name] = value

    return ElicitResult(action="accept", content=content)


# --- LLM и MCP-клиент ---

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    max_retries=2,
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)

client = MultiServerMCPClient(
    {
        "to-do-list": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
        }
    },
    callbacks=Callbacks(
        on_logging_message=on_log,
        on_elicitation=on_elicitation,
    ),
)


# --- LangGraph агент ---

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
            "names": task_lists[0] if task_lists else "Нет списков",
        },
    )
    messages = prompt + state["messages"]
    response = await llm.ainvoke(messages)
    return {"messages": response}


@tool
async def get_tasks(name_list: str) -> str:
    """Просмотреть задачи всех списков через ресурс `to-do://tasks`"""
    blobs = await client.get_resources(server_name="to-do-list", uris=["to-do://tasks"])
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

if __name__ == "__main__":
    result = asyncio.run(
        agent.ainvoke({"messages": "Создай список Покупки и добавь туда хлеб и молоко"})
    )
    print(result["messages"][-1].pretty_print())