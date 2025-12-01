"""
Пример 9: Полный рабочий процесс
Демонстрирует: полный цикл - инициализация, добавление, поиск, удаление
"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

print("=" * 70)
print("ПОЛНЫЙ РАБОЧИЙ ПРОЦЕСС ВЕКТОРНОГО ХРАНИЛИЩА")
print("=" * 70)

# ШАГИ 1: Инициализация
print("\n[ШАГ 1] Инициализация векторного хранилища")
print("─" * 70)
embeddings = DeterministicFakeEmbedding(size=4096)
vector_store = InMemoryVectorStore(embedding=embeddings)
print("✓ Хранилище создано")

# ШАГ 2: Подготовка документов
print("\n[ШАГ 2] Подготовка документов")
print("─" * 70)
documents = [
    Document(
        page_content="Машинное обучение использует алгоритмы и статистику.",
        metadata={"category": "ML", "source": "article"},
    ),
    Document(
        page_content="Нейронные сети имитируют работу мозга.",
        metadata={"category": "DL", "source": "article"},
    ),
    Document(
        page_content="Глубокое обучение — подмножество машинного обучения.",
        metadata={"category": "DL", "source": "research"},
    ),
    Document(
        page_content="Рецепт пиццы требует муку, помидоры и сыр.",
        metadata={"category": "cooking", "source": "recipe"},
    ),
]
print(f"✓ Подготовлено {len(documents)} документов")

# ШАГ 3: Добавление в хранилище
print("\n[ШАГ 3] Добавление документов в хранилище")
print("─" * 70)
doc_ids = [f"doc{i+1}" for i in range(len(documents))]
vector_store.add_documents(documents=documents, ids=doc_ids)
print(f"✓ Документы добавлены с ID: {doc_ids}")

# ШАГ 4: Выполнение поиска
print("\n[ШАГ 4] Выполнение поиска по сходству")
print("─" * 70)
queries = [
    "Что такое машинное обучение?",
    "Как готовить еду?",
]

for query in queries:
    results = vector_store.similarity_search(query, k=2)
    print(f"\n🔍 Запрос: '{query}'")
    print(f"Результаты (k=2):")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content[:50]}...")
        print(f"     Категория: {doc.metadata['category']}")

# ШАГ 5: Удаление документа
print("\n\n[ШАГ 5] Удаление документа из хранилища")
print("─" * 70)
vector_store.delete(ids=["doc4"])
print("✓ Документ 'doc4' (рецепт пиццы) удален")

# ШАГ 6: Проверка результатов
print("\n[ШАГ 6] Проверка результатов после удаления")
print("─" * 70)
query = "интеллект обучение"
results = vector_store.similarity_search(query, k=5)
print(f"🔍 Запрос: '{query}'")
print(f"Найдено результатов: {len(results)}")
for i, doc in enumerate(results, 1):
    print(f"  {i}. {doc.page_content[:50]}...")

print("\n" + "=" * 70)
print("ЗАКЛЮЧЕНИЕ: Рабочий процесс завершен успешно!")
print("=" * 70)
