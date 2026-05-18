"""Демонстрация использования тулов через агент."""
import asyncio

from langchain.agents import create_agent

from client._shared import client, llm


async def demo_tools():
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ТУЛОВ")
    print("=" * 50)

    tools = await client.get_tools()
    print(f"Доступные тулы: {[t.name for t in tools]}\n")

    agent = create_agent(llm, tools)

    query = "Создай список дел с ключом 'learn' и добавь в него задачи: 'Сделать домашнее задание' и 'Выучить стих'"
    print(f"Запрос пользователя: {query}\n")

    async for chunk in agent.astream({"messages": [{"role": "user", "content": query}]}):
        for node, state in chunk.items():
            print(f"[{node}]: {state['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(demo_tools())
