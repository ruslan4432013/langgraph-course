"""
Демонстрация дополнительных методов Runnable

with_retry() - повторяет попытки при ошибках
with_fallbacks() - использует альтернативные runnable при ошибке
bind() - привязывает аргументы к runnable
with_types() - привязывает типы
"""

from langchain_core.runnables import RunnableLambda
import random
import time


# Пример 1: with_retry() - повторные попытки
print("=== with_retry(): Повторные попытки при ошибках ===\n")

attempt_count = 0

def unstable_operation(x: int) -> int:
    """Операция, которая часто падает"""
    global attempt_count
    attempt_count += 1
    
    # Падаем в 70% случаев на первые 2 попытки
    if attempt_count <= 2 and random.random() < 0.7:
        raise ValueError(f"Ошибка на попытке {attempt_count}")
    
    return x * 2


# Создаем runnable с повторными попытками
retry_runnable = RunnableLambda(unstable_operation).with_retry(
    stop_after_attempt=3,
    retry_if_exception_type=(ValueError,)
)

# Пытаемся выполнить операцию
attempt_count = 0
try:
    result = retry_runnable.invoke(5)
    print(f"Успех после {attempt_count} попыток: результат = {result}\n")
except ValueError as e:
    print(f"Ошибка даже после повторных попыток: {e}\n")


# Пример 2: with_fallbacks() - альтернативные runnable
print("=== with_fallbacks(): Альтернативные runnable ===\n")

def primary_service(x: int) -> str:
    """Основной сервис (часто падает)"""
    if random.random() < 0.8:  # Падает в 80% случаев
        raise Exception("Основной сервис недоступен")
    return f"Результат от основного сервиса: {x * 10}"


def fallback_service_1(x: int) -> str:
    """Первый резервный сервис"""
    if random.random() < 0.3:  # Падает в 30% случаев
        raise Exception("Первый резервный сервис недоступен")
    return f"Результат от резерва 1: {x * 5}"


def fallback_service_2(x: int) -> str:
    """Второй резервный сервис (очень надежный)"""
    return f"Результат от резерва 2: {x * 2}"


# Создаем цепочку с fallbacks
robust_chain = (
    RunnableLambda(primary_service).with_fallbacks([
        RunnableLambda(fallback_service_1),
        RunnableLambda(fallback_service_2)
    ])
)

# Проверяем несколько раз
print("Множественные попытки с fallbacks:")
for i in range(5):
    try:
        result = robust_chain.invoke(10)
        print(f"  Попытка {i+1}: {result}")
    except Exception as e:
        print(f"  Попытка {i+1}: Все сервисы недоступны - {e}")
print()


# Пример 3: bind() - привязка аргументов
print("=== bind(): Привязка аргументов ===\n")

def calculate_with_params(value: int, multiplier: int = 1, offset: int = 0) -> int:
    """Вычисление с параметрами"""
    return (value * multiplier) + offset


calc_runnable = RunnableLambda(calculate_with_params)

# Привязываем параметры multiplier и offset
specialized_calc = calc_runnable.bind(multiplier=2, offset=5)

# Теперь invoke принимает только value
result = specialized_calc.invoke(10)
print(f"calculate_with_params(10, multiplier=2, offset=5) = {result}")
print(f"Проверка: (10 * 2) + 5 = 25\n")

# Batch с привязанными параметрами
print("Batch с привязанными параметрами:")
inputs = [1, 2, 3, 4, 5]
results = specialized_calc.batch(inputs)
for inp, res in zip(inputs, results):
    print(f"  {inp} -> {res}")
print()


# Пример 4: Цепочки с bind()
print("=== Цепочки с bind() ===\n")

def format_message(text: str, prefix: str = "", suffix: str = "") -> str:
    """Форматирует сообщение"""
    return f"{prefix}{text}{suffix}"


def to_uppercase(text: str) -> str:
    """Преобразует в верхний регистр"""
    return text.upper()


def add_length_info(text: str) -> str:
    """Добавляет информацию о длине"""
    return f"{text} (длина: {len(text)})"


# Создаем цепочку с привязанными параметрами
message_chain = (
    RunnableLambda(format_message).bind(prefix=">>> ", suffix=" <<<") |
    RunnableLambda(to_uppercase) |
    RunnableLambda(add_length_info)
)

result = message_chain.invoke("hello world")
print(f"Результат цепочки:")
print(f"  '{result}'\n")


# Пример 5: Комбинирование retry и bind
print("=== Комбинирование retry и bind ===\n")

call_count = 0

def api_call(endpoint: str, timeout: int = 5) -> str:
    """Имитирует API вызов"""
    global call_count
    call_count += 1
    
    if call_count <= 2 and random.random() < 0.6:
        raise TimeoutError(f"API timeout на {endpoint}")
    
    return f"API ответ от {endpoint}: данные получены"


# Привязываем параметры API и добавляем повторные попытки
api_runnable = (
    RunnableLambda(api_call)
    .bind(timeout=10)
    .with_retry(
        stop_after_attempt=3,
        retry_if_exception_type=(TimeoutError,)
    )
)

# Пытаемся вызвать API
call_count = 0
try:
    result = api_runnable.invoke("/users")
    print(f"Успех после {call_count} попыток: {result}\n")
except TimeoutError as e:
    print(f"Ошибка: {e}\n")


# Пример 6: with_types() - привязка типов
print("=== with_types(): Привязка типов ===\n")

def flexible_function(input_data):
    """Функция без типов"""
    if isinstance(input_data, dict):
        return f"Обработан словарь с ключами: {list(input_data.keys())}"
    elif isinstance(input_data, list):
        return f"Обработан список из {len(input_data)} элементов"
    else:
        return f"Обработаны данные типа {type(input_data).__name__}"


# Без привязки типов
generic_runnable = RunnableLambda(flexible_function)

# С привязкой типов
typed_runnable = generic_runnable.with_types(
    input_type=dict,
    output_type=str
)

# Оба работают, но с типами будет лучше интеграция с LangServe и IDE
result1 = generic_runnable.invoke({"name": "Alice", "age": 30})
result2 = typed_runnable.invoke({"name": "Bob", "age": 25})

print(f"Без типов: {result1}")
print(f"С типами: {result2}")
