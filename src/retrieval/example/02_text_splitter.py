# https://python.langchain.com/docs/how_to/splitting/

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents([Document(page_content="Длинный текст...")])
print(len(docs))
print(docs[0].page_content)