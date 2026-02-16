#!/bin/bash

set -e  # Остановить скрипт при ошибке

# 1. Проверка наличия .env
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".env created successfully."
    else
        echo "WARNING: .env.example not found!"
    fi
else
    echo ".env already exists."
fi

# 2. Создание виртуального окружения, если его нет
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# 3. Активация виртуального окружения
echo "Activating virtual environment..."
source .venv/bin/activate

# 4. Обновление pip и установка зависимостей
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Запуск LangGraph
echo "Starting LangGraph dev server..."
langgraph dev
