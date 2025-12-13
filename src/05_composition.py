"""
Демонстрация композиции Runnable

Одной из ключевых возможностей интерфейса является декларативная 
композиция runnable в цепочки. Используются операторы | для 
RunnableSequence и словари для RunnableParallel.
"""

from langchain_core.runnables import RunnableLambda


# Пример 1: RunnableSequence - последовательная композиция
print("=== RunnableSequence: Последовательная композиция ===\n")

def add_five(x: int) -> int:
    """Добавляет 5"""
    return x + 5


def multiply_by_two(x: int) -> int:
    """Умножает на 2"""
    return x * 2


def subtract_three(x: int) -> int:
    """Вычитает 3"""
    return x - 3


# Создание последовательности с помощью оператора |
add_runnable = RunnableLambda(add_five)
mul_runnable = RunnableLambda(multiply_by_two)
sub_runnable = RunnableLambda(subtract_three)

# Компонуем: (x + 5) * 2 - 3
sequence = add_runnable | mul_runnable | sub_runnable

# Тестирование
input_value = 10
result = sequence.invoke(input_value)
print(f"Входные данные: {input_value}")
print(f"(10 + 5) * 2 - 3 = {result}")
print(f"Проверка: (10 + 5) * 2 - 3 = 30 - 3 = 27\n")

# Batch для последовательности
print("Batch для последовательности:")
inputs = [1, 2, 3, 4, 5]
results = sequence.batch(inputs)
print(f"Входы: {inputs}")
print(f"Результаты: {results}\n")


# Пример 2: RunnableParallel - параллельная композиция
print("=== RunnableParallel: Параллельная композиция ===\n")

def square(x: int) -> int:
    """Возводит в квадрат"""
    return x ** 2


def cube(x: int) -> int:
    """Возводит в куб"""
    return x ** 3


def double(x: int) -> int:
    """Удваивает"""
    return x * 2


# Создание параллельной композиции используя словарь
parallel = RunnableLambda(lambda x: x) | {
    "squared": RunnableLambda(square),
    "cubed": RunnableLambda(cube),
    "doubled": RunnableLambda(double)
}

result = parallel.invoke(3)
print(f"Входные данные: 3")
print(f"Результат параллельной обработки:")
for key, value in result.items():
    print(f"  {key}: {value}")

print("\nBatch для параллельной композиции:")
inputs = [2, 3, 4]
results = parallel.batch(inputs)
for i, result in enumerate(results):
    print(f"Входное значение {inputs[i]}: {result}\n")


# Пример 3: Смешанная композиция (последовательность + параллель)
print("=== Смешанная композиция ===\n")

# Сначала обрабатываем данные, потом распределяем на параллельные ветви
def prepare_data(x: int) -> int:
    """Подготавливает данные"""
    return x + 10


# Последовательность: подготовка -> параллельная обработка
mixed = RunnableLambda(prepare_data) | {
    "result_a": RunnableLambda(lambda x: x * 2),
    "result_b": RunnableLambda(lambda x: x + 100),
    "result_c": RunnableLambda(lambda x: x ** 2)
}

result = mixed.invoke(5)
print(f"Входные данные: 5")
print(f"Подготовка: 5 + 10 = 15")
print(f"Параллельная обработка 15:")
for key, value in result.items():
    print(f"  {key}: {value}\n")


# Пример 4: Использование метода pipe()
print("=== Использование метода pipe() ===\n")

runnable_a = RunnableLambda(add_five)
runnable_b = RunnableLambda(multiply_by_two)
runnable_c = RunnableLambda(subtract_three)

# Явное использование pipe
pipe_sequence = runnable_a.pipe(runnable_b, runnable_c)

result = pipe_sequence.invoke(10)
print(f"Результат с pipe: {result}")
print(f"Эквивалентно: runnable_a | runnable_b | runnable_c\n")


# Пример 5: Сложная композиция с преобразованием типов
print("=== Сложная композиция с преобразованием типов ===\n")

def string_to_list(s: str) -> list:
    """Преобразует строку в список слов"""
    return s.split()


def count_items(items: list) -> int:
    """Считает количество элементов"""
    return len(items)


def multiply_result(x: int) -> str:
    """Умножает на 10 и преобразует в строку"""
    return f"Result: {x * 10}"


complex_chain = (
    RunnableLambda(string_to_list) | 
    RunnableLambda(count_items) | 
    RunnableLambda(multiply_result)
)

result = complex_chain.invoke("Python LangChain Runnable")
print(f"Входная строка: 'Python LangChain Runnable'")
print(f"1. Разбиваем на слова: ['Python', 'LangChain', 'Runnable']")
print(f"2. Считаем элементы: 3")
print(f"3. Умножаем на 10 и преобразуем: {result}\n")


# Пример 6: Работа с batch для составных цепочек
print("=== Batch для составных цепочек ===\n")

texts = ["Hello World", "Python Code", "AI Runnable"]
text_chain = (
    RunnableLambda(string_to_list) | 
    RunnableLambda(count_items)
)

results = text_chain.batch(texts)
for text, count in zip(texts, results):
    print(f"'{text}' -> {count} слов")
