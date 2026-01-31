"""
Создание инструмента (tool) для retriever с использованием декоратора @tool.

Документация:
- Tools: https://python.langchain.com/docs/concepts/tools/
- Creating Tools: https://python.langchain.com/docs/how_to/custom_tools/
"""

import os
import getpass

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Подготовка данных и retriever
print("📥 Подготовка retriever...")
url = "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
docs = WebBaseLoader(url).load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs)

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()


# Создание инструмента с помощью декоратора @tool
@tool
def retrieve_blog_posts(query: str) -> str:
    """Search and return information about Lilian Weng blog posts."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


# Сохраняем ссылку на инструмент
retriever_tool = retrieve_blog_posts

# Информация об инструменте
print("\n📋 Информация об инструменте:")
print(f"   Имя: {retriever_tool.name}")
print(f"   Описание: {retriever_tool.description}")
print(f"   Схема аргументов: {retriever_tool.args}")

# Тестирование инструмента
print("\n🧪 Тестирование инструмента...")
result = retriever_tool.invoke({"query": "types of reward hacking"})
print(f"\nРезультат (первые 500 символов):\n{result[:500]}...")