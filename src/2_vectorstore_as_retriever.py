from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class DummyVectorStore:
    def __init__(self, documents):
        self._documents = documents

    def similarity_search(self, query, k=2):
        # Заглушка: просто вернуть первые k документов
        return self._documents[:k]

    def as_retriever(self):
        return VectorStoreRetriever(self)


class VectorStoreRetriever(BaseRetriever):
    def __init__(self, vectorstore):
        self._vectorstore = vectorstore

    def _get_relevant_documents(self, query):
        return self._vectorstore.similarity_search(query, k=2)


if __name__ == "__main__":
    docs = [
        Document(page_content="Документ про BM25 и TF-IDF.", metadata={"id": "bm25"}),
        Document(page_content="Документ про векторные хранилища.", metadata={"id": "vec"}),
        Document(page_content="Документ про графовые базы данных.", metadata={"id": "graph"}),
    ]

    vectorstore = DummyVectorStore(docs)
    retriever = vectorstore.as_retriever()

    query = "поиск"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
