# https://python.langchain.com/docs/how_to/retrievers/

from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List

class SimpleRetriever(BaseRetriever):
    docs: List[Document] = [Document(page_content="Пример документа")]

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.docs

retriever = SimpleRetriever()
docs = retriever.invoke("query")
print(docs[0].page_content)