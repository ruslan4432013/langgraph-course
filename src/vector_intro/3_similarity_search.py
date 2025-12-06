"""
Пример 3: Поиск по сходству
Демонстрирует: выполнение семантического поиска в хранилище
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

# Добавление документов
documents = [
    Document(
        page_content="Машинное обучение — это область искусственного интеллекта.",
        metadata={"source": "AI_guide"},
    ),
    Document(
        page_content="Нейронные сети используются для обработки сложных данных.",
        metadata={"source": "AI_guide"},
    ),
    Document(
        page_content="Рецепт блинов: мука, яйца, молоко и сахар.",
        metadata={"source": "recipe"},
    ),
]

vector_store.add_documents(documents=documents, ids=["ai1", "ai2", "recipe1"])

# Выполнение поиска по сходству
query = "искусственный интеллект и нейронные сети"
results = vector_store.similarity_search(query, k=2)

print("✓ Поиск по сходству выполнен")
print(f"Запрос: '{query}'")
print(f"Найдено результатов (k=2):\n")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")
    print(f"   Источник: {doc.metadata['source']}\n")
