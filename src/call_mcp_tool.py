"""
Скрипт для вызова MCP-инструмента SearchDocsByLangChain.

Отправляет JSON-RPC запрос на MCP-сервер LangChain и получает результат поиска
по документации. Поддерживает ответ как в формате JSON, так и в формате SSE (Server-Sent Events).
"""

import asyncio
import json

import aiohttp

# URL MCP-сервера LangChain
MCP_URL = "https://docs.langchain.com/mcp"


async def parse_sse(resp: aiohttp.ClientResponse) -> dict | None:
    """Парсит поток SSE (Server-Sent Events) и возвращает первое JSON-RPC сообщение.

    SSE-поток содержит строки вида:
        event: message
        data: {"jsonrpc": "2.0", ...}

    Функция пропускает служебные строки и извлекает JSON из строки с данными.
    """
    async for raw_line in resp.content:
        line = raw_line.decode("utf-8").strip()
        print(f'{line=}')

        # Пропускаем пустые строки и строки с типом события
        if not line or line.startswith("event:"):
            continue

        # Извлекаем JSON-данные из строки "data: {...}"
        if line.startswith("data:"):
            line = line[len("data:"):].strip()

        return json.loads(line)

    return None


async def call_mcp_tool(query: str) -> dict:
    """Вызывает инструмент SearchDocsByLangChain через MCP-протокол.

    Формирует JSON-RPC запрос, отправляет его на MCP-сервер и возвращает ответ.
    Автоматически определяет формат ответа (JSON или SSE).
    """
    # JSON-RPC запрос к MCP-серверу
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "SearchDocsByLangChain",
            "arguments": {"query": query},
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(MCP_URL, json=payload, headers=headers, ssl=False) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "")

            # Сервер может ответить обычным JSON или потоком SSE
            if "text/event-stream" in content_type:
                return await parse_sse(resp)
            return await resp.json()


async def main():
    result = await call_mcp_tool("how to create a chat agent")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
