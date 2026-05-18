"""Демонстрация загрузки и использования промптов."""
import asyncio

from langchain.agents import create_agent
from langchain_core.tools import tool

from client._shared import client, llm


@tool
async def read_resource(uri: str) -> str:
    """
    Читает содержимое MCP-ресурса по его URI.
    Доступные ресурсы:
      - to-do://lists  — список всех ключей списков дел
      - to-do://tasks  — все задачи по каждому списку
    """
    blobs = await client.get_resources("todo")
    for blob in blobs:
        if str(blob.metadata["uri"]) == uri:
            return blob.as_string()
    available = [str(b.metadata["uri"]) for b in blobs]
    return f"Ресурс '{uri}' не найден. Доступные URI: {available}"


async def demo_prompts():
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ПРОМПТОВ")
    print("=" * 50)

    messages = await client.get_prompt(
        "todo",
        "prompt_to_do_list",
        arguments={"names": "work, personal"},
    )
    print("Загруженный промпт:")
    for msg in messages:
        print(f"  [{msg.type}]: {msg.content}\n")

    mcp_tools = await client.get_tools()
    agent = create_agent(llm, mcp_tools + [read_resource])

    query = "Покажи мне все существующие списки и задачи."
    print(f"Запрос пользователя: {query}\n")

    async for chunk in agent.astream({"messages": messages + [{"role": "user", "content": query}]}):
        for node, state in chunk.items():
            print(f"[{node}]: {state['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(demo_prompts())
