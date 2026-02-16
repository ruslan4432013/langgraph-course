# LangGraph Course - LangChain Quick Start

Этот проект демонстрирует возможности использования LangChain и LangGraph для создания интеллектуальных агентов с
инструментами, памятью и структурированным выводом.

## Основные возможности

- **Создание агентов** через `create_agent`.
- **Инструменты (Tools)**: Использование декоратора `@tool` для определения функций, доступных агенту.
- **Контекст (Context)**: Передача пользовательских данных в инструменты через `ToolRuntime`.
- **Структурированный вывод (Structured Output)**: Использование `dataclass` для получения строго типизированных ответов
  от агента.
- **Память (Persistence)**: Сохранение состояния разговора с помощью `InMemorySaver`.

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <url_репозитория>
   cd langgraph-course
   ```

2. **Настройте виртуальное окружение**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для macOS/Linux
   # или
   .venv\Scripts\activate  # Для Windows
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения**:
   Создайте файл `.env` на основе `.env.example` и заполните его вашими ключами:
   ```bash
   cp .env.example .env
   ```
   Обязательно укажите `OPENAI_API_KEY`. В данном проекте используется прокси `https://api.proxyapi.ru/openai/v1`.

## Быстрый старт (LangChain Quick Start)

Основной пример находится в файле `src/langchain_start/langchain_quick_start.py`. В нем реализован агент-метеоролог,
который:

- Умеет определять местоположение пользователя по его ID.
- Предоставляет прогноз погоды (с каламбурами!).
- Возвращает ответ в строго определенном формате.

### Запуск примера:

```bash
python -m src.langchain_start.langchain_quick_start
```

### Разбор ключевых компонентов примера:

**1. Инструменты с доступом к контексту:**

```python
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Получить информацию о пользователе на основе ID пользователя."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
```

**2. Структурированный ответ:**

```python
@dataclass
class ResponseFormat:
    punny_response: str
    weather_conditions: str | None = None
```

**3. Инициализация агента:**

```python
agent = create_agent(
    model=model,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)
```

## Использование с LangGraph

Проект также подготовлен для работы с LangGraph. Основная точка входа для графа определена в `main.py` и
сконфигурирована в `langgraph.json`.

Запуск через LangGraph CLI (если установлен):

```bash
langgraph dev
```

## Структура проекта

- `src/langchain_start/` — примеры быстрого старта на LangChain.
    - `langchain_quick_start.py` — расширенный пример агента.
    - `basic_agent.py` — базовый пример агента.
- `src/settings.py` — конфигурация настроек через Pydantic.
- `main.py` — точка входа для LangGraph.
- `langgraph.json` — конфигурационный файл для LangGraph Cloud/CLI.
- `requirements.txt` — список зависимостей.
