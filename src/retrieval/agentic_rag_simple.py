import asyncio

import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from src.settings import settings


@tool
def fetch_url(url: str) -> str:
    """Извлечь текстовое содержимое из URL"""
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text


system_prompt = """\
Используй fetch_url, когда нужно получить информацию с веб-страницы; цитируй соответствующие фрагменты.
"""

model = ChatAnthropic(
    model_name="claude-haiku-4-5",
    base_url='https://api.proxyapi.ru/anthropic',
    api_key=settings.OPENAI_API_KEY
)

agent = create_agent(
    model=model,
    tools=[fetch_url],  # Инструмент для поиска
    system_prompt=system_prompt,
)


async def main():
    input_message = HumanMessage(
        content='Получи документацию с https://langchain-ai.github.io/langgraph/llms.txt и скажи, что в ней написано')

    async for chunk in agent.astream({"messages": [input_message]}, stream_mode="updates"):
        for step, data in chunk.items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")


if __name__ == '__main__':
    asyncio.run(main())
