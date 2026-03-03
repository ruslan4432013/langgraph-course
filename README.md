# AI-приложение с клиентом MCP

## Описание

Образовательный проект — клиент **MCP** (Model Context Protocol) на стеке **Python 3.11 / LangChain / LangGraph**.

Агент построен на архитектуре **ReAct** и умеет обращаться к ресурсам, инструментам и промптам
MCP-сервера по ведению списков дел.  
Работает в паре с [MCP-сервером](https://github.com/ruslan4432013/langgraph-course/tree/mcp/server).

## Структура проекта

```
├── scripts/
│   ├── linux.sh            # Скрипт запуска для Linux / macOS
│   └── windows.bat         # Скрипт запуска для Windows
├── src/
│   ├── agent.py            # ReAct-агент с бизнес-логикой
│   ├── settings.py         # Загрузка конфигураций из .env (Pydantic Settings)
│   ├── call_mcp_tool.py    # Вызов MCP-инструмента SearchDocsByLangChain (JSON-RPC / SSE)
│   └── get_tools.py        # Получение списка инструментов с MCP-сервера
├── .env.example            # Шаблон переменных окружения
├── .env                    # Переменные окружения (не коммитится)
├── langgraph.json          # Конфигурация LangGraph / LangSmith
├── requirements.txt        # Зависимости Python
└── README.md
```

## Требования

1. **Python 3.11** (или совместимая версия).
2. Заполненный файл **`.env`** (см. `.env.example`).
3. Запущенный [MCP-сервер](https://github.com/ruslan4432013/langgraph-course/tree/mcp/server).

## Переменные окружения

Скопируйте `.env.example` → `.env` и заполните значения:

| Переменная           | Описание                                           |
|----------------------|----------------------------------------------------|
| `LANGSMITH_TRACING`  | Включение трассировки LangSmith (`true` / `false`) |
| `LANGSMITH_ENDPOINT` | URL эндпоинта LangSmith                            |
| `LANGSMITH_API_KEY`  | API-ключ LangSmith                                 |
| `LANGSMITH_PROJECT`  | Название проекта в LangSmith                       |
| `OPENAI_API_KEY`     | API-ключ OpenAI (или прокси)                       |
| `OPENAI_BASE_URL`    | Базовый URL OpenAI API (необязательно)             |
| `TAVILY_API_KEY`     | API-ключ Tavily для веб-поиска                     |

## Запуск

Склонируйте репозиторий, перейдите в корневую директорию и выполните:

**Linux / macOS:**

```bash
./scripts/linux.sh
```

**Windows:**

```bat
scripts\windows.bat
```

Скрипт автоматически:

1. Создаст `.env` из `.env.example` (если отсутствует).
2. Создаст виртуальное окружение `.venv`.
3. Установит зависимости из `requirements.txt`.
4. Запустит dev-сервер LangGraph (`langgraph dev`).

## Утилиты

| Скрипт                 | Описание                                                                                                        |
|------------------------|-----------------------------------------------------------------------------------------------------------------|
| `src/call_mcp_tool.py` | Пример вызова MCP-инструмента `SearchDocsByLangChain` — отправляет JSON-RPC запрос и парсит ответ (JSON / SSE). |
| `src/get_tools.py`     | Получает список доступных инструментов с MCP-сервера и сохраняет в `tools.json`.                                |

Запуск утилит:

```bash
source .venv/bin/activate
python src/call_mcp_tool.py
python src/get_tools.py
```

## Примеры работы

![Пример работы агента](img/example.png)
