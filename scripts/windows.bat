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

REM 4. Запускаем сервер
.\.venv\Scripts\python.exe -m src.main
