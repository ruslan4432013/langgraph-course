"""
Пример 8: Параметры поиска similarity_search
Демонстрирует: использование параметров k и других опций
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from src.settings import settings

# Инициализация модели
embeddings_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)
vector_store = InMemoryVectorStore(embedding=embeddings_model)

# Добавление множества документов
documents = [
    Document(
        page_content=f"Документ о Python номер {i}",
        metadata={"index": i, "type": "tutorial"},
    )
    for i in range(1, 11)
]

vector_store.add_documents(
    documents=documents, ids=[f"doc{i}" for i in range(1, 11)]
)

query = "Python программирование"

print("=" * 60)
print("ПАРАМЕТРЫ ПОИСКА (similarity_search)")
print("=" * 60)

print(f"\n📝 Запрос: '{query}'\n")

# Демонстрация параметра k
for k_value in [1, 3, 5]:
    results = vector_store.similarity_search(query, k=k_value)
    print(f"\n{'─' * 60}")
    print(f"Результаты с k={k_value} (количество результатов):")
    print(f"{'─' * 60}")
    print(f"Найдено результатов: {len(results)}")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")

print(f"\n{'=' * 60}")
print("ОСНОВНЫЕ ПАРАМЕТРЫ:")
print("=" * 60)
print("""
• query (str): Текст для поиска
• k (int): Количество результатов для возврата (по умолчанию 4)
• filter (dict): Условия фильтрации по метаданным

Примечание: Полный набор параметров зависит от конкретного
векторного хранилища. Некоторые хранилища могут поддерживать
дополнительные параметры для большего контроля над поиском.
""")
