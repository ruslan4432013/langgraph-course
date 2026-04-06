@echo off

REM 1. Создаём виртуальное окружение, если его нет
if not exist ".venv" (
    echo Создаём виртуальное окружение...
    python -m venv .venv
) else (
    echo Виртуальное окружение уже существует
)

REM 2. Активируем виртуальное окружение
call .venv\Scripts\activate.bat

REM 3. Устанавливаем зависимости
echo Устанавливаем зависимости...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Создаём .env из .env.example, если его нет
if not exist ".env" (
    if exist ".env.example" (
        echo Создаём .env из .env.example...
        copy .env.example .env > nul
    ) else (
        echo ВНИМАНИЕ: .env.example не найден!
    )
) else (
    echo .env уже существует
)

REM 5. Запускаем dev-сервер
langgraph dev
