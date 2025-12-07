"""
Демонстрация трёх основных метрик сходства:
- Косинусное сходство
- Евклидово расстояние
- Скалярное произведение
"""

import math


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Косинусное сходство: косинус угла между векторами (от -1 до 1)"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (norm1 * norm2)


def euclidean_distance(vec1: list[float], vec2: list[float]) -> float:
    """Евклидово расстояние: прямая линия между точками (чем меньше, тем ближе)"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def dot_product(vec1: list[float], vec2: list[float]) -> float:
    """Скалярное произведение: проекция одного вектора на другой"""
    return sum(a * b for a, b in zip(vec1, vec2))


# Пример с простыми векторами для наглядности
vec_a = [1.0, 0.0, 0.0]  # Направлен по оси X
vec_b = [0.0, 1.0, 0.0]  # Направлен по оси Y (перпендикулярен)
vec_c = [1.0, 0.0, 0.0]  # Идентичен vec_a
vec_d = [0.7, 0.7, 0.0]  # Между X и Y (под углом 45°)

print("=== Сравнение идентичных векторов (vec_a и vec_c) ===")
# print(f"Косинусное сходство: {cosine_similarity(vec_a, vec_c):.4f}")  # 1.0
# print(f"Евклидово расстояние: {euclidean_distance(vec_a, vec_c):.4f}")  # 0.0
print(f"Скалярное произведение: {dot_product(vec_a, vec_c):.4f}")  # 1.0

print("\n=== Сравнение перпендикулярных векторов (vec_a и vec_b) ===")
# print(f"Косинусное сходство: {cosine_similarity(vec_a, vec_b):.4f}")  # 0.0
# print(f"Евклидово расстояние: {euclidean_distance(vec_a, vec_b):.4f}")  # ~1.41
print(f"Скалярное произведение: {dot_product(vec_a, vec_b):.4f}")  # 0.0
#
print("\n=== Сравнение похожих векторов (vec_a и vec_d) ===")
# print(f"Косинусное сходство: {cosine_similarity(vec_a, vec_d):.4f}")  # ~0.71
# print(f"Евклидово расстояние: {euclidean_distance(vec_a, vec_d):.4f}")  # ~0.76
print(f"Скалярное произведение: {dot_product(vec_a, vec_d):.4f}")  # 0.7
