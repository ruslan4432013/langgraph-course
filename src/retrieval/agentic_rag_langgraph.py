import asyncio

import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from src.settings import settings


@tool
def fetch_documentation(url: str) -> str:
    """Извлечь и преобразовать документацию из URL"""

    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text


# Предварительная загрузка содержимого llms.txt

system_prompt = f"""
Ты эксперт-разработчик на Python и технический помощник.
Твоя основная роль — помогать пользователям с вопросами с Anthropic.

Чтоб ответить на вопрос пользователя у тебя есть ссылки на документацию, используй ее, так как тут самая свежая информация:
https://platform.claude.com/docs/en/get-started.md
https://platform.claude.com/docs/en/about-claude/models/overview.md
https://platform.claude.com/docs/en/about-claude/models/choosing-a-model.md

Используй fetch_documentation чтоб получить информацию.
"""

tools = [fetch_documentation]
model = ChatAnthropic(
    model_name="claude-haiku-4-5",
    base_url='https://api.proxyapi.ru/anthropic',
    api_key=settings.OPENAI_API_KEY
)

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    name="Agentic RAG",
)


async def main():
    get_info_input = HumanMessage('Как выбрать правильную модель anthropic?')

    async for chunk in agent.astream({"messages": [get_info_input]}, stream_mode="updates"):
        for step, data in chunk.items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")


if __name__ == '__main__':
    asyncio.run(main())
