#!/bin/bash
set -e

# 1. Создаём виртуальное окружение, если его нет
if [ ! -d ".venv" ]; then
    echo "Создаём виртуальное окружение..."
    python3 -m venv .venv
else
    echo "Виртуальное окружение уже существует"
fi

# 2. Активируем виртуальное окружение
echo "Активируем виртуальное окружение..."
source .venv/bin/activate

# 3. Устанавливаем зависимости
echo "Устанавливаем зависимости..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Запускаем сервер
python -m src.main
