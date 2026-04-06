import asyncio

from fastmcp import Client
from fastmcp.client.logging import LogMessage
from fastmcp.client.sampling.handlers.openai import OpenAISamplingHandler
from openai import AsyncOpenAI

from src.settings import settings


# Обработчик логов
async def log_handler(message: LogMessage):
    print(f"[{message.level}] {message.data}")


# Обработчик эликитации — автоматически подтверждает все запросы
async def elicitation_handler(message, response_type, params, context):
    print(f"\n[elicitation] {message}")
    print("[elicitation] Автоматическое подтверждение")
    return {}


# Обработчик sampling — использует OpenAI-совместимый API
sampling_handler = OpenAISamplingHandler(
    default_model="gpt-4o",
    client=AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL or None,
    ),
)


async def main():
    async with Client(
        "http://localhost:8000/mcp",
        sampling_handler=sampling_handler,
        elicitation_handler=elicitation_handler,
        log_handler=log_handler,
    ) as client:
        # Просмотр доступных инструментов
        tools = await client.list_tools()
        for tool in tools:
            print(f"Tool: {tool.name} - {tool.description}")

        # Сначала создаём список
        result = await client.call_tool(
            "init_to_do_list",
            {"name_list": "Учёба"},
        )
        print(result)

        # Вызов инструмента с sampling — LLM генерирует задачи
        result = await client.call_tool(
            "generate_tasks",
            {"list_name": "Учёба", "topic": "подготовка к экзамену по Python"},
        )
        print(result)


if __name__ == "__main__":
    print("sampling (генерация задач через LLM) ===\n")
    asyncio.run(main())
