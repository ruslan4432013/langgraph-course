from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

from src.settings import settings

api_key = settings.PROXY_API_KEY


llm_openai = ChatOpenAI(
    model='gpt-5.5',
    base_url='https://api.proxyapi.ru/openai/v1',
    temperature=0,
    api_key=api_key
)

llm_anthropic = init_chat_model(
    model="claude-haiku-4-5",
    temperature=0,
    api_key=api_key,
    base_url="https://api.proxyapi.ru/anthropic",
    model_provider='anthropic'
)

llm_google = init_chat_model(
    model="gemini-3.1-pro-preview",
    temperature=0,
    api_key=api_key,
    base_url="https://api.proxyapi.ru/google",
    model_provider='google_genai'
)

llm_qwen = init_chat_model(
    model='minimax/minimax-m2.7',
    base_url='https://api.proxyapi.ru/openrouter/v1',
    api_key=api_key,
    model_provider='openai'
)


if __name__ == "__main__":
    result_anthropic = llm_qwen.invoke("Hello, who are you?")
    print(result_anthropic.content)
