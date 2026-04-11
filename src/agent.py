import asyncio

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import Callbacks
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from mcp.types import ElicitResult

from src.settings import settings
from src.oauth_handler import create_oauth_provider


# --- Callbacks для MCP ---

async def on_log(params, context):
    """Обработчик логов от MCP-сервера."""
    print(f"  [{params.level}] ({context.server_name}) {params.data}")


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

        value = input(f"  {title}: ")

        # Приведение типов
        if field_schema.get("type") == "integer":
            value = int(value)
        elif field_schema.get("type") == "boolean":
            value = value.lower() in ("true", "1", "yes", "y")

        content[field_name] = value

    return ElicitResult(action="accept", content=content)


# --- OAuth и MCP-клиент ---

oauth = create_oauth_provider()

client = MultiServerMCPClient(
    {
        "to-do-list": {
            "transport": "http",
            "url": f"{settings.MCP_SERVER_URL}/mcp",
            "auth": oauth,
        },
    },
    callbacks=Callbacks(
        on_logging_message=on_log,
        on_elicitation=on_elicitation,
    ),
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL or None,
)


# --- LangGraph агент ---

class State(MessagesState):
    pass


async def call_llm(state: State) -> State:
    """Вызов LLM с системным промптом и инструментами."""
    system = (
        "Ты — помощник для управления списками дел. "
        "Используй доступные инструменты."
    )
    messages = [{"role": "system", "content": system}] + state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": response}


tools = asyncio.run(client.get_tools())
llm_with_tools = llm.bind_tools(tools)
call_tools = ToolNode(tools=tools)

graph = StateGraph(State)
graph.add_node("model", call_llm)
graph.add_node("tools", call_tools)
graph.add_edge(START, "model")
graph.add_conditional_edges("model", tools_condition)
graph.add_edge("tools", "model")

agent = graph.compile()


if __name__ == "__main__":
    async def main():
        print("\nАгент готов. Введите запрос (или 'выход' для завершения):\n")

        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() in ("выход", "exit", "quit"):
                print("До свидания!")
                break

            result = await agent.ainvoke({"messages": [("user", user_input)]})
            response = result["messages"][-1].content
            print(f"\nАгент: {response}\n")

    asyncio.run(main())
