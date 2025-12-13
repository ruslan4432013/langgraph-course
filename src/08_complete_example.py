"""
Полный практический пример: Построение полноценной цепочки Runnable

Демонстрирует:
- Композицию runnable
- Параллельную обработку
- Обработку ошибок
- Конфигурацию
- Пакетную обработку
"""

from langchain_core.runnables import RunnableLambda, RunnableGenerator
import json


# ==================== Определение компонентов ====================

def validate_email(email: str) -> dict:
    """Валидирует email"""
    if "@" not in email or "." not in email:
        raise ValueError(f"Некорректный email: {email}")
    return {"email": email, "valid": True}


def extract_domain(email: str) -> str:
    """Извлекает домен из email"""
    return email.split("@")[1]


def check_domain_reputation(domain: str) -> dict:
    """Проверяет репутацию домена"""
    trusted_domains = ["gmail.com", "outlook.com", "yandex.ru", "mail.ru"]
    is_trusted = domain in trusted_domains
    return {
        "domain": domain,
        "trusted": is_trusted,
        "reputation_score": 0.95 if is_trusted else 0.6
    }


def count_string_length(text: str) -> int:
    """Считает длину строки"""
    return len(text)


def check_password_strength(password: str) -> dict:
    """Проверяет надежность пароля"""
    checks = {
        "has_upper": any(c.isupper() for c in password),
        "has_lower": any(c.islower() for c in password),
        "has_digit": any(c.isdigit() for c in password),
        "has_special": any(c in "!@#$%^&*" for c in password),
        "length_ok": len(password) >= 8
    }
    strength = sum(checks.values()) / len(checks) * 100
    return {
        "checks": checks,
        "strength_percent": strength,
        "is_strong": strength >= 80
    }


def prepare_user_registration(email: str) -> dict:
    """Подготавливает данные пользователя"""
    return {
        "email": email,
        "registered_at": "2024-01-15",
        "status": "active"
    }


# ==================== Построение цепочек ====================

print("=== Пример 1: Простая последовательность ===\n")

# Создаем простую цепочку валидации email
email_chain = (
    RunnableLambda(validate_email) |
    RunnableLambda(lambda result: result["email"]) |
    RunnableLambda(extract_domain)
)

try:
    domain = email_chain.invoke("user@gmail.com")
    print(f"Домен из email: {domain}\n")
except Exception as e:
    print(f"Ошибка: {e}\n")


# ==================== Параллельная обработка ====================

print("=== Пример 2: Параллельная проверка email ===\n")

# Параллельная обработка: валидация -> (извлечение домена + проверка репутации)
parallel_email_chain = (
    RunnableLambda(lambda email: email) |
    {
        "domain": RunnableLambda(extract_domain),
        "domain_info": RunnableLambda(extract_domain) | RunnableLambda(check_domain_reputation),
        "email_length": RunnableLambda(count_string_length)
    }
)

result = parallel_email_chain.invoke("user@gmail.com")
print(f"Параллельная обработка email:")
print(json.dumps(result, ensure_ascii=False, indent=2))
print()


# ==================== Обработка пароля ===

print("=== Пример 3: Проверка надежности пароля ===\n")

password_chain = (
    RunnableLambda(check_password_strength) |
    RunnableLambda(lambda result: f"Надежность: {result['strength_percent']:.0f}% - {'Сильный' if result['is_strong'] else 'Слабый'}")
)

passwords = ["weak", "Medium123", "Strong@Pass123", "VeryStr0ng!Pwd"]
print("Проверка паролей:")
for pwd in passwords:
    result = password_chain.invoke(pwd)
    print(f"  '{pwd}': {result}")
print()


# ==================== Batch обработка ===

print("=== Пример 4: Batch обработка нескольких email ===\n")

emails = [
    "alice@gmail.com",
    "bob@outlook.com",
    "charlie@unknown.com",
    "diana@yandex.ru"
]

# Цепочка для обработки одного email
single_email_chain = (
    RunnableLambda(extract_domain) |
    RunnableLambda(check_domain_reputation) |
    RunnableLambda(lambda result: f"{result['domain']}: {'Проверенный' if result['trusted'] else 'Неизвестный'}")
)

# Batch обработка
results = single_email_chain.batch(emails)
print("Batch обработка email адресов:")
for email, result in zip(emails, results):
    print(f"  {email}: {result}")
print()


# ==================== Сложная композиция ===

print("=== Пример 5: Полная регистрация пользователя ===\n")

def create_user_profile(data: dict) -> dict:
    """Создает профиль пользователя"""
    return {
        "email": data["email"],
        "user_id": data["email"].replace("@", "_").replace(".", "_"),
        "registered_at": data["registered_at"],
        "status": data["status"]
    }


def convert_to_json(data: dict) -> str:
    """Преобразует в JSON"""
    return json.dumps(data, ensure_ascii=False, indent=2)


# Полная цепочка регистрации
registration_chain = (
    RunnableLambda(prepare_user_registration) |
    RunnableLambda(create_user_profile) |
    RunnableLambda(convert_to_json)
)

result = registration_chain.invoke("newuser@gmail.com")
print("Профиль нового пользователя:")
print(result)
print()


# ==================== Использование конфигурации ===

print("=== Пример 6: Обработка с конфигурацией ===\n")

# Создаем цепочку с конфигурацией
config_chain = RunnableLambda(check_domain_reputation)

# Batch с конфигурацией
domains = ["gmail.com", "yahoo.com", "yandex.ru"]
results = config_chain.batch(
    domains,
    config={
        "run_name": "domain_reputation_check",
        "tags": ["security", "validation"],
        "metadata": {"check_date": "2024-01-15"},
        "max_concurrency": 2
    }
)

print("Проверка репутации доменов с конфигурацией:")
for domain, result in zip(domains, results):
    print(f"  {domain}: {result['reputation_score']*100:.0f}% репутация")
print()


# ==================== Обработка ошибок ===

print("=== Пример 7: Обработка ошибок в batch ===\n")

test_emails = [
    "valid@gmail.com",
    "invalid-email",
    "another@yahoo.com",
    "bad@format"
]

validation_chain = RunnableLambda(validate_email)

# Batch с обработкой ошибок
results = validation_chain.batch(
    test_emails,
    return_exceptions=True
)

print("Валидация email адресов (с обработкой ошибок):")
for email, result in zip(test_emails, results):
    if isinstance(result, Exception):
        print(f"  {email}: ❌ {result}")
    else:
        print(f"  {email}: ✓ {result['valid']}")
print()


# ==================== Генератор ===

print("=== Пример 8: RunnableGenerator для отчета ===\n")

def generate_validation_report(emails: list):
    """Генератор для создания отчета по валидации"""
    yield "=== Отчет валидации email ==="
    yield f"Всего email: {len(emails)}"
    yield ""
    
    for i, email in enumerate(emails, 1):
        try:
            validate_email(email)
            yield f"{i}. {email}: ✓ Валидный"
        except ValueError:
            yield f"{i}. {email}: ✗ Некорректный"


report_runnable = RunnableGenerator(generate_validation_report)

test_emails = ["user@gmail.com", "invalid", "admin@example.com"]
print("Сгенерированный отчет:")
for line in report_runnable.stream(test_emails):
    print(f"  {line}")
