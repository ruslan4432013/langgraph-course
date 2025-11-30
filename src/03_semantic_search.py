"""
Практический пример: поиск документов по смыслу, а не по ключевым словам.
Демонстрирует главную ценность эмбеддингов.
"""

import math

from langchain_openai import OpenAIEmbeddings

from src.settings import settings


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot_product / (norm1 * norm2)


# Инициализация модели
embeddings_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)

# База документов
documents = [
    "Кошки - это домашние животные семейства кошачьих",
    "Python используется для анализа данных",
    "Собаки считаются лучшими друзьями человека",
    "JavaScript работает в браузере",
    "Хомяки - популярные домашние питомцы",
    "Machine Learning требует больших датасетов",
]

# Создаём эмбеддинги документов
doc_embeddings = embeddings_model.embed_documents(documents)

# Поисковый запрос (обратите внимание - слов "кошка" и "собака" нет!)
query = "Какие бывают домашние любимцы?"
query_embedding = embeddings_model.embed_query(query)

# Вычисляем сходство запроса с каждым документом
similarities = []
for i, doc_emb in enumerate(doc_embeddings):
    sim = cosine_similarity(query_embedding, doc_emb)
    similarities.append((sim, documents[i]))

# Сортируем по убыванию сходства
similarities.sort(reverse=True)

print(f"Запрос: '{query}'\n")
print("Результаты поиска (по релевантности):")
print("-" * 50)
for score, doc in similarities:
    print(f"[{score:.4f}] {doc}")
