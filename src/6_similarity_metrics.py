"""
Пример 6: Демонстрация концепции метрик сходства
Показывает вычисление основных метрик сходства между векторами
"""

import math

def cosine_similarity(vec1, vec2):
    """Вычисление косинусного сходства"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 != 0 else 0

def euclidean_distance(vec1, vec2):
    """Вычисление евклидова расстояния"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

def dot_product(vec1, vec2):
    """Вычисление скалярного произведения"""
    return sum(a * b for a, b in zip(vec1, vec2))

# Примеры векторов
vector_a = [1.0, 0.5, 0.2]
vector_b = [0.9, 0.6, 0.1]
vector_c = [0.1, 0.1, 0.8]

print("=" * 60)
print("МЕТРИКИ СХОДСТВА МЕЖДУ ВЕКТОРАМИ")
print("=" * 60)

print(f"\nВектор A: {vector_a}")
print(f"Вектор B: {vector_b}")
print(f"Вектор C: {vector_c}")

print("\n" + "-" * 60)
print("СРАВНЕНИЕ А и В (похожие векторы):")
print("-" * 60)
print(f"Косинусное сходство:  {cosine_similarity(vector_a, vector_b):.4f}")
print(f"  (значение близко к 1 означает высокое сходство)")
print(f"Евклидово расстояние: {euclidean_distance(vector_a, vector_b):.4f}")
print(f"  (меньшее значение означает большее сходство)")
print(f"Скалярное произведение: {dot_product(vector_a, vector_b):.4f}")

print("\n" + "-" * 60)
print("СРАВНЕНИЕ А и С (менее похожие векторы):")
print("-" * 60)
print(f"Косинусное сходство:  {cosine_similarity(vector_a, vector_c):.4f}")
print(f"  (значение ближе к 0 означает низкое сходство)")
print(f"Евклидово расстояние: {euclidean_distance(vector_a, vector_c):.4f}")
print(f"  (большее значение означает меньшее сходство)")
print(f"Скалярное произведение: {dot_product(vector_a, vector_c):.4f}")

print("\n" + "=" * 60)
print("ВЫВОДЫ:")
print("=" * 60)
print("• Косинусное сходство: используется для измерения угла между векторами")
print("• Евклидово расстояние: измеряет прямолинейное расстояние")
print("• Скалярное произведение: проекция одного вектора на другой")
print("\nВекторные хранилища используют эти метрики для поиска похожих документов.")
