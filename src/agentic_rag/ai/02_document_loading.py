"""
Загрузка документов с использованием WebBaseLoader.

Документация:
- Document Loaders: https://python.langchain.com/docs/concepts/document_loaders/
- WebBaseLoader: https://python.langchain.com/docs/integrations/document_loaders/web_base/
"""

from langchain_community.document_loaders import WebBaseLoader

# URL-адреса для загрузки (блог Lilian Weng)
urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

# Загрузка документов
print("📥 Загрузка документов...")
docs = [WebBaseLoader(url).load() for url in urls]

# Проверка загруженных документов
print(f"\n✅ Загружено {len(docs)} документов")

for i, doc_list in enumerate(docs):
    doc = doc_list[0]
    print(f"\n--- Документ {i + 1} ---")
    print(f"Источник: {doc.metadata.get('source', 'N/A')}")
    print(f"Длина контента: {len(doc.page_content)} символов")
    print(f"Превью (первые 500 символов):\n{doc.page_content.strip()[:500]}...")