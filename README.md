# MCP-сервер (ToDo-список) с GitHub OAuth

MCP-сервер разработан с использованием [официального SDK](https://gofastmcp.com/) и демонстрирует аутентификацию через GitHub OAuth с использованием встроенного `GitHubProvider` из FastMCP.

## Структура проекта

| Путь | Описание |
|---|---|
| `./scripts` | Скрипты для запуска проекта |
| `./main.py` | Точка входа |
| `./server.py` | Конфигурация сервера + GitHubProvider |
| `./src/primitive/` | Tools, Resources и Prompts |
| `./src/service/` | Бизнес-логика (ToDoList с per-user данными) |
| `./src/settings.py` | Настройки (GitHub OAuth credentials, BASE_URL) |

## Что добавлено в этом уроке

- **GitHub OAuth** — `GitHubProvider` из FastMCP автоматически создаёт все OAuth-эндпоинты (discovery, DCR, authorize, callback, token)
- **Dependency Injection** — `CurrentAccessToken()` для получения OAuth-токена в инструментах
- **Изоляция данных** — каждый пользователь видит только свои списки дел (`user_id` из JWT)

## Перед запуском

1. Зарегистрируйте OAuth App на GitHub (Settings → Developer settings → OAuth Apps)
2. Создайте `.env` из `.env.example` и заполните `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`

## Запуск

1. Клонируйте репозиторий и перейдите в корень проекта
2. Выполните скрипт запуска:

```bash
# Linux / macOS
./scripts/linux.sh

# Windows
scripts\windows.bat
```

Сервер запустится на `http://localhost:8000/mcp`.
