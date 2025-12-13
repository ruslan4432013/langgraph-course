"""
Демонстрация пользовательских Runnable

RunnableLambda - оборачивает функцию и предоставляет стандартные методы
invoke и batch, а также интеграцию с конфигурацией и трассировкой.

RunnableGenerator - оборачивает генератор для потоковой передачи данных.
"""

from langchain_core.runnables import RunnableLambda, RunnableGenerator


# Пример 1: Базовое использование RunnableLambda
print("=== RunnableLambda: Базовое использование ===\n")

def calculate_area(radius: float) -> float:
    """Вычисляет площадь круга"""
    pi = 3.14159
    return pi * radius ** 2


# Оборачиваем функцию в RunnableLambda
area_runnable = RunnableLambda(calculate_area)

# Используем invoke
result = area_runnable.invoke(5.0)
print(f"Площадь круга с радиусом 5: {result:.2f}\n")

# Используем batch
radii = [1.0, 2.0, 3.0, 4.0, 5.0]
areas = area_runnable.batch(radii)
print(f"Площади кругов для радиусов {radii}:")
for r, a in zip(radii, areas):
    print(f"  Радиус {r}: {a:.2f}")
print()


# Пример 2: RunnableLambda с преобразованием типов
print("=== RunnableLambda с преобразованием типов ===\n")

def process_person_data(data: dict) -> str:
    """Обрабатывает данные человека и возвращает приветствие"""
    name = data.get("name", "Гость")
    age = data.get("age", "неизвестного")
    return f"Привет, {name}! Тебе {age} лет."


person_runnable = RunnableLambda(process_person_data)

# Invoke с словарем
person_data = {"name": "Алиса", "age": 28}
result = person_runnable.invoke(person_data)
print(f"Результат: {result}\n")

# Batch с несколькими словарями
people_data = [
    {"name": "Боб", "age": 35},
    {"name": "Виктория", "age": 42},
    {"name": "Глеб"}
]
results = person_runnable.batch(people_data)
for result in results:
    print(result)
print()


# Пример 3: RunnableGenerator для потоковой передачи
print("=== RunnableGenerator: Потоковая передача ===\n")

def count_to_n(n: int):
    """Генератор, выдающий числа от 1 до n"""
    for i in range(1, n + 1):
        yield f"Число {i}"


# Оборачиваем генератор в RunnableGenerator
counter_runnable = RunnableGenerator(count_to_n)

# Используем stream для получения результатов по одному
print("Результаты из генератора (stream):")
for item in counter_runnable.stream(5):
    print(f"  - {item}")
print()


# Пример 4: RunnableGenerator с обработкой данных
print("=== RunnableGenerator: Обработка списка ===\n")

def process_items_stream(items: list):
    """Генератор, обрабатывающий список элементов"""
    for i, item in enumerate(items, 1):
        processed = item.upper() if isinstance(item, str) else str(item)
        yield f"[{i}] {processed}"


items_runnable = RunnableGenerator(process_items_stream)

# Stream для обработки списка
items = ["python", "langchain", "runnable"]
print("Обработка элементов:")
for result in items_runnable.stream(items):
    print(f"  {result}")
print()


# Пример 5: Композиция RunnableLambda
print("=== Композиция RunnableLambda ===\n")

def text_to_uppercase(text: str) -> str:
    """Преобразует в верхний регистр"""
    return text.upper()


def count_characters(text: str) -> int:
    """Считает символы"""
    return len(text)


def create_report(count: int) -> str:
    """Создает отчет"""
    return f"Текст содержит {count} символов"


# Создаем цепочку: строка -> вверхний регистр -> подсчет -> отчет
text_chain = (
    RunnableLambda(text_to_uppercase) |
    RunnableLambda(count_characters) |
    RunnableLambda(create_report)
)

result = text_chain.invoke("hello world")
print(f"Входная строка: 'hello world'")
print(f"1. HELLO WORLD")
print(f"2. Длина: 11")
print(f"3. {result}\n")


# Пример 6: RunnableLambda с конфигурацией
print("=== RunnableLambda с конфигурацией ===\n")

def greet_user(name: str) -> str:
    """Приветствует пользователя"""
    return f"Добро пожаловать, {name}!"


greeting_runnable = RunnableLambda(greet_user)

# Invoke с конфигурацией
result = greeting_runnable.invoke(
    "Иван",
    config={
        "run_name": "greeting_run",
        "tags": ["greeting", "user_interaction"],
        "metadata": {"user_id": "ivan_001", "timestamp": "2024-01-01"}
    }
)
print(f"Результат: {result}")
print(f"Конфигурация сохранена для отслеживания\n")


# Пример 7: RunnableLambda для обработки ошибок
print("=== RunnableLambda с обработкой ошибок ===\n")

def safe_division(data: dict) -> str:
    """Безопасное деление"""
    try:
        a = data.get("a", 0)
        b = data.get("b", 1)
        result = a / b
        return f"Результат: {result:.2f}"
    except ZeroDivisionError:
        return "Ошибка: деление на ноль!"


safe_div_runnable = RunnableLambda(safe_division)

# Тестирование с разными данными
test_cases = [
    {"a": 10, "b": 2},
    {"a": 15, "b": 0},
    {"a": 20, "b": 4}
]

print("Безопасное деление:")
results = safe_div_runnable.batch(test_cases)
for data, result in zip(test_cases, results):
    print(f"  {data['a']} / {data['b']}: {result}")
