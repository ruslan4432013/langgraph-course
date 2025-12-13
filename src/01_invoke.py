"""
Демонстрация метода invoke - синхронный вызов одного входа

invoke преобразует один вход в выход. Используется для базовых примеров, 
отладки и когда требуется получить детерминированный результат для конкретного входа.
"""

from langchain_core.runnables import RunnableLambda


def add_ten(x: int) -> int:
    """Функция, которая добавляет 10 к входу"""
    return x + 10


# Создаем runnable из функции
runnable = RunnableLambda(add_ten)

# Базовое использование invoke - вызов одного входа
result = runnable.invoke(5)
print(f"invoke(5) = {result}")  # Результат: 15

# Использование invoke с конфигурацией
result_with_config = runnable.invoke(
    20,
    config={
        "run_name": "my_addition_run",
        "tags": ["arithmetic", "addition"],
        "metadata": {"operation": "add_ten"}
    }
)
print(f"invoke(20) с конфигурацией = {result_with_config}")  # Результат: 30

# Пример с более сложной функцией
def multiply_and_add(x: int) -> int:
    """Умножаем на 3 и добавляем 5"""
    return x * 3 + 5


complex_runnable = RunnableLambda(multiply_and_add)
result_complex = complex_runnable.invoke(4)
print(f"multiply_and_add(4) = {result_complex}")  # Результат: 4 * 3 + 5 = 17
