#!/bin/bash

# 1. Создание виртуального окружения, если его нет
if [ ! -d ".venv" ]; then
    echo "Create virtual venv..."
    python -m venv .venv
else
    echo "Virtual venv is exists"
fi

# 2. Активация виртуального окружения
echo "Активируем виртуальное окружение..."
source .venv/bin/activate

# 3. Обновление pip и установка зависимостей
echo "Download dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

./.venv/Scripts/python.exe -m src.main