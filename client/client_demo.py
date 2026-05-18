"""
Демонстрационный LangChain клиент для MCP сервера To-Do List.

Запуск сервера перед использованием:
    python -m src.main

Запуск клиента:
    python -m client.client_demo
"""

import asyncio

from client.demo_tools import demo_tools
from client.demo_resources import demo_resources
from client.demo_prompts import demo_prompts


async def main():
    print("Запуск демонстрации MCP клиента для To-Do List сервера")

    await demo_tools()
    await demo_resources()
    await demo_prompts()

    print("\n" + "=" * 50)
    print("Демонстрация завершена!")


if __name__ == "__main__":
    asyncio.run(main())
