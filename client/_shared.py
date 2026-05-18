"""Общие объекты: LLM и MCP клиент."""

from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient

from client.settings import settings

llm = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    api_key=settings.PROXY_API_KEY.get_secret_value(),
    base_url="https://api.proxyapi.ru/anthropic",
)

client = MultiServerMCPClient(
    {
        "todo": {
            "transport": "sse",
            "url": "http://localhost:8000/sse",
        }
    }
)
