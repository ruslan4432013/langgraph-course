"""
Пример 2: Добавление документов в хранилище
Демонстрирует: создание Document объектов и их добавление в хранилище
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

embeddings = DeterministicFakeEmbedding(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)

# Создание документов
document_1 = Document(
    page_content="Я ел блинчики с шоколадной стружкой и яичницу на завтрак этим утром.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="Прогноз погоды на завтра — облачно и пасмурно, с максимумом в 62 градуса.",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="Python — мощный язык программирования для анализа данных.",
    metadata={"source": "article"},
)

documents = [document_1, document_2, document_3]

# Добавление документов с явными ID
vector_store.add_documents(documents=documents, ids=["doc1", "doc2", "doc3"])

print("✓ Документы добавлены в хранилище")
print(f"Количество документов: {len(documents)}")
print("\nДобавленные документы:")
for doc_id, doc in zip(["doc1", "doc2", "doc3"], documents):
    print(f"  {doc_id}: {doc.page_content[:50]}... (source: {doc.metadata['source']})")
