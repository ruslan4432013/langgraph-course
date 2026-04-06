import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.callbacks import Callbacks
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from mcp.types import ElicitResult

from src.settings import settings


# --- Callbacks ---

async def on_log(params, context):
    print(f"[{params.level}] ({context.server_name}) {params.data}")


async def on_elicitation(mcp_context, params, context):
    print(f"\n--- Запрос от сервера ({context.server_name}) ---")
    print(f"Сообщение: {params.message}")

    if not params.requestedSchema or not params.requestedSchema.get("properties"):
        answer = input("Подтвердить? (y/n): ").strip().lower()
        if answer == "y":
            return ElicitResult(action="accept", content={})
        else:
            return ElicitResult(action="decline")

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


# --- Агент ---

tools = asyncio.run(client.get_tools())

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "Ты - помощник, который помогает пользователю управлять списками дел. "
        "Используй доступные инструменты для создания списков и добавления задач."
    ),
)

if __name__ == "__main__":
    result = asyncio.run(
        agent.ainvoke({
            "messages": [
                {"role": "user", "content": "Создай список Покупки и добавь туда хлеб, молоко и яйца"}
            ]
        })
    )
    print(result["messages"][-1].content)
