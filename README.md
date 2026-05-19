# AI-приложение с клиентом MCP

## Описание

Клиент создан на стеке Python/LangChain/LangGraph в образовательных целях. Реализует агента на архитектуре ReAct, который подключается к MCP-серверу по ведению списков дел.

Агент умеет:
- Создавать новые списки дел через инструмент `init_to_do_list`
- Добавлять задачи через инструмент `add_task_to_do_list`
- Читать списки и задачи через MCP-ресурсы (`to-do://lists`, `to-do://tasks`)
- Использовать системный промпт с сервера для контекстуализации запросов

> **Важно:** Транспорт SSE (Server-Sent Events) устарел. В этом уроке используется **Streamable HTTP транспорт** (`http://localhost:8000/mcp`).

## Структура проекта

```
.
├── src/
│   ├── client/                # MCP-клиент (агент)
│   │   ├── agent.py           # LangGraph-агент с бизнес-логикой
│   │   └── settings.py        # Загрузка конфигураций из .env
│   └── server/                # MCP-сервер (из предыдущего урока)
│       ├── server.py          # Создание экземпляра FastMCP
│       ├── main.py            # Точка входа сервера (HTTP транспорт)
│       ├── primitive/
│       │   ├── tools.py       # MCP-инструменты (init_to_do_list, add_task_to_do_list)
│       │   ├── resources.py   # MCP-ресурсы (to-do://lists, to-do://tasks)
│       │   └── prompts.py     # MCP-промпты (prompt_to_do_list)
│       ├── service/
│       │   └── to_do_list.py  # Бизнес-логика работы с JSON-хранилищем
│       └── data/
│           └── to_do_list.json # JSON-файл с данными списков дел
├── scripts/
│   ├── linux.sh               # Скрипт запуска для Linux/macOS
│   └── windows.bat            # Скрипт запуска для Windows
├── langgraph.json             # Конфигурация LangGraph/LangSmith
├── .env.example               # Пример файла с переменными окружения
└── requirements.txt           # Зависимости проекта
```

## Требования перед запуском

1. Python 3.11+ в системе
2. Заполненный `.env` файл (скопировать из `.env.example`)
3. Запущенный MCP-сервер на `http://localhost:8000`

## Настройка окружения

Скопировать `.env.example` в `.env` и заполнить:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="<ваш ключ от LangSmith>"
LANGSMITH_PROJECT="<название проекта в LangSmith>"
PROXY_API_KEY="<ваш ключ от ProxyAPI>"
```

## Запуск

### Шаг 1 — Запустить MCP-сервер (из предыдущего урока)

MCP-сервер находится в директории `server/` этого же проекта. Запустить его в **отдельном терминале**:

```bash
# Из корня проекта
python -m src.server.main
```

Сервер запустится на `http://localhost:8000`. Убедиться, что он работает:

```bash
curl http://localhost:8000/mcp
```

### Шаг 2 — Запустить клиента (агента)

**Linux / macOS:**
```bash
./scripts/linux.sh
```

**Windows:**
```bat
scripts\windows.bat
```

Скрипт автоматически:
1. Создаст виртуальное окружение `.venv`
2. Установит зависимости из `requirements.txt`
3. Запустит `langgraph dev` для работы с агентом через LangGraph Studio

### Запуск агента напрямую (без LangGraph Studio)

```bash
# Из корня проекта с активированным виртуальным окружением
python -m src.client.agent
```

Агент выполнит два тестовых запроса:
1. Добавит задачи в список (хлеб, молоко, яйца)
2. Запросит, что нужно купить в магазине

## Как работает агент

```
Пользователь → [LangGraph Agent]
                      |
              [call_llm node]
                |         |
    get_resources()    get_prompt()   ← MCP-ресурсы и промпты
                      |
              [Claude LLM]
                      |
          tools_condition (нужны инструменты?)
               /              \
         [tools node]        [END]
    init_to_do_list()
    add_task_to_do_list()
    get_tasks()          ← MCP-инструменты
               \
          [model node] → [END]
```

1. При каждом вызове LLM агент забирает актуальные списки дел с сервера (`to-do://lists`)
2. Получает с сервера системный промпт с именами доступных списков
3. LLM решает, нужно ли вызывать инструменты (создать список, добавить задачу, прочитать задачи)
4. После вызова инструментов цикл возвращается к LLM

## Примеры запуска

![](img/example.png)
