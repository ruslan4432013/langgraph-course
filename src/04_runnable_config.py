"""
Демонстрация RunnableConfig - конфигурация выполнения

RunnableConfig управляет поведением runnable при выполнении и трассировкой.
Включает параметры: run_name, run_id, tags, metadata, max_concurrency, 
recursion_limit, configurable, callbacks.
"""

import uuid
from langchain_core.runnables import RunnableLambda


# Пример 1: Базовое использование конфигурации
print("=== Базовая конфигурация ===\n")

def process_data(x: int) -> int:
    """Простая функция обработки"""
    return x * 2


runnable = RunnableLambda(process_data)

# Использование конфигурации
result = runnable.invoke(
    10,
    config={
        "run_name": "multiplication_run",
        "tags": ["math", "doubling"],
        "metadata": {"user_id": "user_123", "operation": "multiply_by_2"}
    }
)
print(f"Результат: {result}")
print(f"Конфигурация была применена к запуску\n")


# Пример 2: Использование run_id
print("=== Использование run_id ===\n")

# Генерируем уникальный ID для отслеживания запуска
run_id = str(uuid.uuid4())
print(f"Уникальный ID запуска: {run_id}\n")

result = runnable.invoke(
    5,
    config={
        "run_id": run_id,
        "run_name": "tracked_run",
        "tags": ["important"],
        "metadata": {"batch_id": "batch_001"}
    }
)
print(f"Результат: {result}")
print(f"Этот запуск можно отследить по ID: {run_id}\n")


# Пример 3: Использование max_concurrency с batch
print("=== max_concurrency при пакетной обработке ===\n")

import time

def slow_processing(x: int) -> int:
    """Медленная обработка"""
    time.sleep(0.5)
    return x ** 2


slow_runnable = RunnableLambda(slow_processing)
inputs = [1, 2, 3, 4]

# Без ограничения параллелизма
print("Batch без ограничения параллелизма:")
start = time.time()
results = slow_runnable.batch(inputs)
print(f"Время: {time.time() - start:.2f} сек\n")

# С ограничением параллелизма до 2
print("Batch с max_concurrency=2:")
start = time.time()
results = slow_runnable.batch(
    inputs,
    config={"max_concurrency": 2}
)
print(f"Время: {time.time() - start:.2f} сек\n")


# Пример 4: Использование configurable для гибкой конфигурации
print("=== Конфигурируемые параметры ===\n")

def multiply_by_factor(x: int, factor: int = 2) -> int:
    """Умножение на коэффициент"""
    return x * factor


configurable_runnable = RunnableLambda(multiply_by_factor)

# Использование configurable для передачи параметров
result = configurable_runnable.invoke(
    10,
    config={
        "configurable": {"factor": 5}
    }
)
print(f"10 * 5 = {result}\n")


# Пример 5: Метаданные и теги для отладки
print("=== Метаданные и теги для организации запусков ===\n")

def analyze_text(text: str) -> dict:
    """Анализирует текст"""
    return {
        "length": len(text),
        "words": len(text.split()),
        "uppercase_count": sum(1 for c in text if c.isupper())
    }


analysis_runnable = RunnableLambda(analyze_text)

# Используем теги и метаданные для классификации запуска
result = analysis_runnable.invoke(
    "Hello World Python Programming",
    config={
        "run_name": "text_analysis",
        "tags": ["nlp", "text_processing", "production"],
        "metadata": {
            "version": "1.0",
            "model": "text_analyzer_v1",
            "priority": "high",
            "user_group": "premium"
        }
    }
)

print(f"Результаты анализа: {result}")
print(f"Запуск помечен как производственный с высоким приоритетом\n")


# Пример 6: Передача одной конфигурации для всех входов в batch
print("=== Одинаковая конфигурация для batch ===\n")

texts = ["Python", "Java", "JavaScript"]
shared_config = {
    "run_name": "batch_analysis",
    "tags": ["programming_languages"],
    "metadata": {"batch_number": 1}
}

results = analysis_runnable.batch(texts, config=shared_config)
for text, result in zip(texts, results):
    print(f"{text}: {result}")
