import asyncio
import json

import aiohttp

MCP_URL = 'https://docs.langchain.com/mcp'


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(MCP_URL, ssl=False) as response:
            html = await response.json()
            print(html)
            with open('tools.json', 'w') as f:
                json.dump(html, f)


if __name__ == "__main__":
    asyncio.run(main())
