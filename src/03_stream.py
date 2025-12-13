"""
Демонстрация методов stream и astream - потоковая передача

stream возвращает итератор по частям результата. Используется для реализации 
прогрессивного вывода в пользовательском интерфейсе.
astream - асинхронный аналог stream.
"""

from langchain_core.runnables import RunnableLambda


# Пример 1: Простая потоковая передача
print("=== Stream: Построчный вывод ===\n")

def generate_greeting(name: str) -> str:
    """Генерирует приветствие"""
    return f"Привет, {name}! Это сообщение для потоковой передачи."


greeting_runnable = RunnableLambda(generate_greeting)

# Stream по умолчанию вызывает invoke и возвращает весь результат
# Здесь мы эмулируем посимвольный вывод
result = greeting_runnable.invoke("Мир")
for char in result:
    print(char, end="", flush=True)
print("\n")


# Пример 2: Потоковая передача со списками
print("=== Stream: Обработка списков ===\n")

def process_list_as_stream(numbers: list[int]) -> str:
    """Обрабатывает список и возвращает результат построчно"""
    results = []
    for num in numbers:
        results.append(f"Число: {num}, Квадрат: {num**2}")
    return "\n".join(results)


list_runnable = RunnableLambda(process_list_as_stream)
result = list_runnable.invoke([1, 2, 3, 4, 5])
print(result)


# Пример 3: Асинхронный stream
print("\n=== Асинхронный Stream ===\n")

import asyncio


async def async_stream_example():
    """Демонстрирует асинхронный stream"""
    
    async def async_operation(x: int) -> str:
        """Асинхронная операция"""
        await asyncio.sleep(0.1)
        return f"Обработана задача для {x}"
    
    async_runnable = RunnableLambda(async_operation)
    
    # astream возвращает асинхронный итератор
    async for result in async_runnable.astream(5):
        print(f"Результат: {result}")


# Раскомментируйте для запуска асинхронного примера
# asyncio.run(async_stream_example())


# Пример 4: Генератор с потоковой передачей
print("\n=== RunnableGenerator: Истинная потоковая передача ===\n")

from langchain_core.runnables import RunnableGenerator


def number_generator(n: int):
    """Генератор, выдающий числа от 1 до n"""
    for i in range(1, n + 1):
        yield f"Число {i}"


generator_runnable = RunnableGenerator(number_generator)

# Используем stream для получения результатов
print("Результаты из генератора:")
for item in generator_runnable.stream(5):
    print(f"  - {item}")


# Пример 5: Комбинирование stream с конвейерами
print("\n=== Stream в конвейере ===\n")

def add_prefix(text: str) -> str:
    """Добавляет префикс к тексту"""
    return f"[ОБРАБОТАНО] {text}"


# Создаем конвейер: генератор -> преобразование
pipeline = generator_runnable | RunnableLambda(add_prefix)

# Используем batch для обработки потока
results = pipeline.batch([3, 2])
print(f"Результаты конвейера: {results}")
