from langchain_openai import ChatOpenAI

from src.settings import settings

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1",
    api_key=settings.API_KEY
)
