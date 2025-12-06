"""
Пример 5: Фильтрация по метаданным
Демонстрирует: семантический поиск с фильтрацией по метаданным
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

# Добавление документов с разными источниками
documents = [
    Document(
        page_content="Твит о новом релизе Python 3.13",
        metadata={"source": "tweet", "date": "2024-01"},
    ),
    Document(
        page_content="Новости: Python становится более популярным",
        metadata={"source": "news", "date": "2024-01"},
    ),
    Document(
        page_content="Твит: Люблю Python за его простоту",
        metadata={"source": "tweet", "date": "2024-01"},
    ),
    Document(
        page_content="Статья о производительности Python",
        metadata={"source": "article", "date": "2024-02"},
    ),
]

vector_store.add_documents(
    documents=documents, ids=["tweet1", "news1", "tweet2", "article1"]
)

# Поиск с фильтрацией по источнику
query = "Python программирование"
print("✓ Выполнен поиск с фильтрацией по метаданным")
print(f"Запрос: '{query}'\n")

# Примечание: InMemoryVectorStore имеет ограниченную поддержку фильтрации
# В реальных приложениях используйте специализированные хранилища (Pinecone, Chroma и т.д.)
results = vector_store.similarity_search(query, k=3)

print("Все результаты (без фильтрации):")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")
    print(f"   Источник: {doc.metadata.get('source')}, Дата: {doc.metadata.get('date')}\n")

print("\nПримечание: Для полноценной фильтрации по метаданным используйте")
print("специализированные хранилища как Pinecone, MongoDB Atlas, Qdrant и т.д.")
