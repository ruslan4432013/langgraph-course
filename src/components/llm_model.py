from langchain_openai import ChatOpenAI

from ..settings import settings

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url='https://api.proxyapi.ru/openai/v1',
    model="gpt-5.2",
)
