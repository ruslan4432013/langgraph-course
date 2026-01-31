"""
Создание векторного хранилища и retriever для семантического поиска.

Документация:
- Vector Stores: https://python.langchain.com/docs/concepts/vectorstores/
- Embeddings: https://python.langchain.com/docs/concepts/embedding_models/
- InMemoryVectorStore: https://python.langchain.com/docs/integrations/vectorstores/in_memory/
- OpenAI Embeddings: https://python.langchain.com/docs/integrations/text_embedding/openai/
"""

import os
import getpass

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# Настройка API-ключа
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# 1. Загрузка и разделение документов
print("📥 Загрузка документов...")
url = "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
docs = WebBaseLoader(url).load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs)
print(f"✅ Подготовлено {len(doc_splits)} чанков")

# 2. Создание векторного хранилища с OpenAI embeddings
print("\n🔢 Создание векторного хранилища...")
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=OpenAIEmbeddings()
)
print("✅ Векторное хранилище создано")

# 3. Создание retriever
retriever = vectorstore.as_retriever()

# 4. Тестирование семантического поиска
print("\n🔍 Тестирование поиска...")
query = "types of reward hacking"
results = retriever.invoke(query)

print(f"\nЗапрос: '{query}'")
print(f"Найдено документов: {len(results)}")

for i, doc in enumerate(results):
    print(f"\n--- Результат {i + 1} ---")
    print(f"Контент: {doc.page_content[:300]}...")