from dataclasses import dataclass
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

# ✅ Загружаем ключ из .env файла
load_dotenv()

# Определение системного промпта
SYSTEM_PROMPT = """Вы эксперт по прогнозированию погоды, говорящий каламбурами.

У вас есть доступ к двум инструментам:
- get_weather_for_location: используйте для получения погоды в конкретном месте
- get_user_location: используйте для получения местоположения пользователя

Если пользователь спрашивает о погоде, убедитесь, что известно местоположение. Если из вопроса ясно, что имеется в виду текущее местоположение, используйте инструмент get_user_location для его определения."""


# Определение схемы контекста
@dataclass
class Context:
    """Схема пользовательского контекста выполнения."""
    user_id: str


# Определение инструментов
@tool
def get_weather_for_location(city: str) -> str:
    """Получить погоду для заданного города."""
    return f"В {city} всегда солнечно!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Получить информацию о пользователе на основе ID пользователя."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


# Конфигурация модели
model = init_chat_model(
    model="openai:gpt-4o",
    temperature=0
)


# Определение формата ответа
@dataclass
class ResponseFormat:
    """Схема ответа для агента."""
    # Каламбурный ответ (обязательный)
    punny_response: str
    # Любая интересная информация о погоде, если доступна
    weather_conditions: str | None = None


# Настройка памяти
checkpointer = InMemorySaver()

# Создание агента
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# Запуск агента
# `thread_id` — уникальный идентификатор для разговора.
config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "какая погода на улице?"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])

# Можно продолжить разговор, используя тот же `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "спасибо!"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])