from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

from src.settings import settings

api_key = settings.OPENROUTER_API_KEY


llm_openai = ChatOpenAI(
    model='openai/gpt-5.5',
    base_url='https://openrouter.ai/api/v1',
    temperature=0,
    api_key=api_key
) # +

llm_anthropic = init_chat_model(
    model="anthropic/claude-opus-4.7",
    temperature=0,
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model_provider='openai'
)

llm_google = ChatOpenAI(
    model="google/gemini-3.1-pro-preview",
    temperature=0,
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

llm_qwen = ChatOpenAI(
    model='minimax/minimax-m2.7',
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)


if __name__ == "__main__":
    result_anthropic = llm_anthropic.invoke("Hello, who are you?")
    print(result_anthropic.content)
