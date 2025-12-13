"""
Демонстрация метода batch - пакетная обработка

batch предназначен для параллельной обработки нескольких независимых входов. 
По умолчанию использует пул потоков для эффективного выполнения операций, 
ограниченных вводом-выводом. Возвращает результаты в том же порядке, что и входы.
"""

import time
from langchain_core.runnables import RunnableLambda


def slow_operation(x: int) -> int:
    """Функция с задержкой - имитирует операцию ввода-вывода"""
    time.sleep(0.1)  # Имитируем задержку в 0.1 секунд (например, API запрос)
    return x * 2


# Создаем runnable
runnable = RunnableLambda(slow_operation)

# Список входов для обработки
inputs = [1, 2, 3, 4, 5]

# Пакетная обработка
print("=== Пакетная обработка (batch) ===")
start_time = time.time()
results = runnable.batch(inputs)
batch_time = time.time() - start_time

print(f"Входы: {inputs}")
print(f"Результаты: {results}")
print(f"Время выполнения batch: {batch_time:.2f} сек")

# Пакетная обработка с ограничением параллелизма
print("\n=== Batch с max_concurrency=2 ===")
start_time = time.time()
results_limited = runnable.batch(
    inputs,
    config={"max_concurrency": 2}
)
limited_time = time.time() - start_time

print(f"Результаты: {results_limited}")
print(f"Время выполнения с ограничением: {limited_time:.2f} сек")

# Обработка ошибок в batch
print("\n=== Batch с обработкой ошибок ===")

def sometimes_fails(x: int) -> int:
    """Функция, которая иногда падает"""
    if x == 3:
        raise ValueError(f"Ошибка обработки значения {x}")
    return x * 2


failing_runnable = RunnableLambda(sometimes_fails)

# С return_exceptions=True ошибки будут включены в результаты
results_with_errors = failing_runnable.batch(
    [1, 2, 3, 4, 5],
    return_exceptions=True
)

print("Результаты с ошибками:")
for i, result in enumerate(results_with_errors):
    if isinstance(result, Exception):
        print(f"  Input {i+1}: Ошибка - {result}")
    else:
        print(f"  Input {i+1}: {result}")
