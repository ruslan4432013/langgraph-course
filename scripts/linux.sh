#!/bin/bash
set -e

# 1. Создаём .env из .env.example, если его нет
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Создаём .env из .env.example..."
        cp .env.example .env
    else
        echo "ВНИМАНИЕ: .env.example не найден!"
    fi
else
    echo ".env уже существует"
fi

# 2. Создаём виртуальное окружение, если его нет
if [ ! -d ".venv" ]; then
    echo "Создаём виртуальное окружение..."
    python3 -m venv .venv
else
    echo "Виртуальное окружение уже существует"
fi

# 3. Активируем виртуальное окружение
echo "Активируем виртуальное окружение..."
source .venv/bin/activate

# 4. Устанавливаем зависимости
echo "Устанавливаем зависимости..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Запускаем dev-сервер
langgraph dev
