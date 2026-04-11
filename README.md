# AI-приложение с клиентом MCP и OAuth

Клиент создан на стеке Python 3.11 / LangChain / LangGraph в учебных целях. Работает в тандеме с [MCP-сервером](../server/).

ReAct-агент с автоматической OAuth-аутентификацией через GitHub. Поддерживает два варианта: полный граф (`StateGraph`) и упрощённый (`create_agent()`).

## Структура проекта

| Путь | Описание |
|---|---|
| `./scripts` | Скрипты для запуска проекта |
| `./src/agent.py` | Агент на StateGraph с OAuth |
| `./src/agent_langchain.py` | Упрощённый агент через create_agent() с OAuth |
| `./src/oauth_handler.py` | OAuthClientProvider + callback-сервер |
| `./src/settings.py` | Загрузка конфигурации |
| `./.env` | Файл конфигурации |
| `./langgraph.json` | Конфигурация для langgraph dev |

## Перед запуском

1. Заполненный файл `.env` (создайте из `.env.example`)
2. Установленный Python 3.11
3. Запущенный MCP-сервер (из папки `server/`)

## Запуск

Клонируйте проект, перейдите в корень и выполните:

```bash
# Linux / macOS
./scripts/linux.sh

# Windows
scripts\windows.bat
```

### Запуск через LangGraph Studio

```bash
langgraph dev
```

При первом запуске автоматически откроется браузер для авторизации через GitHub.
