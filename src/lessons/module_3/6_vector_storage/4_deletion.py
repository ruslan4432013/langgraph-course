"""
Пример 4: Удаление документов
Демонстрирует: удаление документов из хранилища по ID
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

embeddings = DeterministicFakeEmbedding(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

# Добавление документов
documents = [
    Document(page_content="Документ 1: Введение в Python", metadata={"type": "intro"}),
    Document(page_content="Документ 2: Продвинутые техники", metadata={"type": "advanced"}),
    Document(page_content="Документ 3: Лучшие практики", metadata={"type": "practices"}),
]

vector_store.add_documents(documents=documents, ids=["doc1", "doc2", "doc3"])

print("✓ Документы добавлены")
print(f"Всего документов до удаления: {len(documents)}")

# Удаление документа
vector_store.delete(ids=["doc2"])

print("✓ Документ 'doc2' удален")

# Проверка: попытка поиска
remaining_results = vector_store.similarity_search("Python", k=5)
print(f"Оставшихся документов в хранилище: {len(remaining_results)}")
print("\nОставшиеся документы:")
for doc in remaining_results:
    print(f"  - {doc.page_content}")
