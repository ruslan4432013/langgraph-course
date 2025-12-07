"""
Демонстрация базового интерфейса моделей эмбеддингов LangChain.
Два основных метода: embed_documents() и embed_query()
"""

from langchain_openai import OpenAIEmbeddings

from src.settings import settings

# Инициализация модели (требуется OPENAI_API_KEY)
embeddings_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)

# 1. Эмбеддинг нескольких документов
documents = [
    "Машинное обучение - это подраздел искусственного интеллекта",
    "Python - популярный язык программирования",
    "Нейронные сети имитируют работу мозга",
    "Data Science использует статистику и программирование",
    "Deep Learning - это глубокое обучение"
]

doc_embeddings = embeddings_model.embed_documents(documents)

print(f"Количество документов: {len(doc_embeddings)}")
print(f"Размерность вектора: {len(doc_embeddings[0])}")
print(f"Первые 5 значений первого вектора: {doc_embeddings[0][:5]}")

# 2. Эмбеддинг одного запроса
query = "Что такое искусственный интеллект?"
query_embedding = embeddings_model.embed_query(query)

print(f"\nРазмерность вектора запроса: {len(query_embedding)}")
print(f"Первые 5 значений: {query_embedding[:5]}")
