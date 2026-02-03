from langchain_openai import ChatOpenAI

from src.settings import settings

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url='https://api.proxyapi.ru/openai/v1',
    model="gpt-5.2",
)

if __name__ == "__main__":
    print(llm.invoke('Hello!'))
