from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class SimpleInMemoryRetriever(BaseRetriever):
    def __init__(self, documents):
        self._documents = documents

    def _get_relevant_documents(self, query):
        # Простейший фильтр: вернуть все документы, где запрос входит в текст
        result = []
        for doc in self._documents:
            if query.lower() in doc.page_content.lower():
                result.append(doc)
        return result


if __name__ == "__main__":
    docs = [
        Document(page_content="Ретриверы используются в RAG-сценариях.", metadata={"id": 1}),
        Document(page_content="Векторные хранилища позволяют искать по смыслу.", metadata={"id": 2}),
    ]

    retriever = SimpleInMemoryRetriever(docs)

    query = "ретриверы"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
