"""
Разделение документов на чанки с использованием RecursiveCharacterTextSplitter.

Документация:
- Text Splitters: https://python.langchain.com/docs/concepts/text_splitters/
- RecursiveCharacterTextSplitter: https://python.langchain.com/docs/how_to/recursive_text_splitter/
"""

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Загрузка документов (упрощённый пример с одним URL)
url = "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
docs = WebBaseLoader(url).load()

print(f"📄 Загружен документ: {len(docs[0].page_content)} символов")

# Создание разделителя текста
# chunk_size=100 — размер чанка в токенах
# chunk_overlap=50 — перекрытие между чанками
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=50
)

# Разделение документов
doc_splits = text_splitter.split_documents(docs)

print(f"\n✅ Документ разделён на {len(doc_splits)} чанков")

# Демонстрация первых 3 чанков
for i, chunk in enumerate(doc_splits[:3]):
    print(f"\n--- Чанк {i + 1} ---")
    print(f"Контент: {chunk.page_content.strip()[:200]}...")
    print(f"Метаданные: {chunk.metadata}")

# Статистика по размерам чанков
chunk_lengths = [len(chunk.page_content) for chunk in doc_splits]
print(f"\n📊 Статистика чанков:")
print(f"   Минимальный размер: {min(chunk_lengths)} символов")
print(f"   Максимальный размер: {max(chunk_lengths)} символов")
print(f"   Средний размер: {sum(chunk_lengths) / len(chunk_lengths):.0f} символов")