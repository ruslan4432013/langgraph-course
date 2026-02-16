@echo off

REM 1. Создание виртуального окружения, если его нет
if not exist ".venv" (
    echo Create virtual venv...
    python -m venv .venv
) else (
    echo Virtual venv already exists
)

REM 2. Активация виртуального окружения
call .venv\Scripts\activate.bat

REM 3. Установка зависимостей
echo Install dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Создание .env из .env.example если его нет
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env > nul
    ) else (
        echo WARNING: .env.example not found!
    )
) else (
    echo .env already exists
)

REM 5. Запуск dev сервера
langgraph dev
