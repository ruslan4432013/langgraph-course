# https://python.langchain.com/docs/how_to/document_loader/

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

loader = TextLoader("example.txt")
documents = loader.load()

# Создание Document вручную
doc = Document(page_content="Текст документа", metadata={"source": "manual"})
print(doc.page_content)  # Вывод: Текст документа
print(doc.metadata)      # Вывод: {'source': 'manual'}