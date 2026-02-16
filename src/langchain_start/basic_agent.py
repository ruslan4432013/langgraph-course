from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from src.settings import settings


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


llm = init_chat_model(
    model="gpt-4.1",
    base_url="https://api.proxyapi.ru/openai/v1",
    api_key=settings.OPENAI_API_KEY
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )

    print(result)
    agent_response = result['messages'][-1]
    print(agent_response.content)
