from dotenv import load_dotenv
from langchain.agents import create_agent

# ✅ Загружаем ключ из .env файла
load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# или другие модели openai:gpt-4o "openai:gpt-4-turbo", "openai:gpt-3.5-turbo"
agent = create_agent(
    model="openai:gpt-4o",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)