"""
Пример 1: Инициализация векторного хранилища
Демонстрирует: создание экземпляра InMemoryVectorStore с моделью эмбеддингов
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import OpenAIEmbeddings

# Инициализация с фальшивой моделью эмбеддингов для демонстрации
embeddings = OpenAIEmbeddings(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

print("✓ Векторное хранилище инициализировано")
print(f"Тип хранилища: {type(vector_store).__name__}")
