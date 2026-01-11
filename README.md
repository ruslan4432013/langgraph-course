# Учебный пример: Сокращение и фильтрация сообщений на LangChain

Этот проект демонстрирует различные способы управления историей сообщений в LangChain и LangGraph. Это критически важно
для эффективного использования контекстного окна LLM и снижения затрат.

## Основные возможности

В проекте рассматриваются три основных подхода к управлению сообщениями:

1. **Ручная фильтрация в графе**: Использование специального типа сообщений `RemoveMessage` для удаления старых записей
   из состояния (`MessagesState`).
2. **Фильтрация при вызове модели**: Передача только части истории сообщений непосредственно перед вызовом LLM (
   например, последних N сообщений).
3. **Обрезка сообщений (Trimming)**: Использование встроенной функции `trim_messages` для умного сокращения истории по
   количеству токенов с сохранением структуры диалога.

## Структура проекта

* `src/main.py` — основной файл с примерами реализации графов и логики управления сообщениями.
* `src/settings.py` — конфигурация проекта с использованием Pydantic Settings.
* `langgraph.json` — конфигурация для LangGraph CLI/Studio.
* `requirements.txt` — список необходимых библиотек.

## Установка

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для macOS/Linux
   # или
   .venv\Scripts\activate     # Для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

Создайте файл `.env` в корне проекта (или используйте существующий) и добавьте туда ваши API ключи. Пример содержимого:

```env
OPENAI_API_KEY=your_openai_api_key

# Настройки LangSmith (опционально)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT="langgraph-course"
```

*Примечание: В коде `src/main.py` настроен базовый URL для работы через прокси. Вы можете изменить его в
инициализации `ChatOpenAI`.*

## Запуск

### Локальный запуск скрипта

Для запуска основного примера выполните команду из корня проекта:

```bash
python -m src.main
```

### Использование LangGraph CLI/Studio

Проект настроен для работы с LangGraph Studio. Вы можете запустить локальный сервер для визуализации и отладки графа:

```bash
# Убедитесь, что установлены зависимости и langgraph-cli
langgraph dev
```

Конфигурация графа определена в `langgraph.json` и указывает на `src/main.py:graph`.

## Ключевые концепции

### Обрезка сообщений (Trimming)

Пример использования функции `trim_messages` в узле графа:

```python
messages = trim_messages(
    state["messages"],
    max_tokens=50,
    strategy="last",
    token_counter=llm,
    allow_partial=False,
)
```

### Фильтрация сообщений

Удаление сообщений из состояния графа через `RemoveMessage`:

```python
def filter_messages(state: MessagesState):
    # Оставляем только последние 2 сообщения
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}
```

---
Учебный проект по изучению возможностей LangGraph и LangChain.
