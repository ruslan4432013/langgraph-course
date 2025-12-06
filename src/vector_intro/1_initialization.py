"""
Пример 1: Инициализация векторного хранилища
Демонстрирует: создание экземпляра InMemoryVectorStore с моделью эмбеддингов
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from src.settings import settings

# Инициализация модели
embeddings_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)
vector_store = InMemoryVectorStore(embedding=embeddings_model)

print("✓ Векторное хранилище инициализировано")
print(f"Тип хранилища: {type(vector_store).__name__}")
