"""
Пример 1: Инициализация векторного хранилища
Демонстрирует: создание экземпляра InMemoryVectorStore с моделью эмбеддингов
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import DeterministicFakeEmbedding

# Инициализация с фальшивой моделью эмбеддингов для демонстрации
embeddings = DeterministicFakeEmbedding(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

print("✓ Векторное хранилище инициализировано")
print(f"Тип хранилища: {type(vector_store).__name__}")
