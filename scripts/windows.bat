@echo off
REM 1. Создание виртуального окружения, если его нет
if not exist ".venv" (
    echo Create virtual venv...
    python -m venv .venv
) else (
    echo Virtual venv us exists
)

REM 2. Активация виртуального окружения
call .venv\Scripts\activate.bat

REM 3. Установка зависимостей из requirements.txt
echo Download dependencies...
pip install --upgrade pip
pip install -r requirements.txt

.\.venv\Scripts\python.exe -m src.main