from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class SimpleLexicalRetriever(BaseRetriever):
    def __init__(self, documents):
        super().__init__()
        self._documents = documents

    def _score(self, query, text):
        # Очень грубая «оценка» по количеству совпавших слов
        query_tokens = query.lower().split()
        text_tokens = text.lower().split()
        return sum(1 for token in query_tokens if token in text_tokens)

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun):
        scored = []
        for doc in self._documents:
            score = self._score(query, doc.page_content)
            scored.append((score, doc))
        # Сортировка по убыванию «оценки», имитация BM25/TF-IDF
        scored.sort(key=lambda x: x[0], reverse=True)
        # Возвращаем только документы с положительным score
        return [doc for score, doc in scored if score > 0]


if __name__ == "__main__":
    docs = [
        Document(page_content="BM25 — алгоритм лексического поиска.", metadata={"id": "bm25"}),
        Document(page_content="TF-IDF также относится к лексическому поиску.", metadata={"id": "tfidf"}),
        Document(page_content="Векторные хранилища ищут по смыслу.", metadata={"id": "vec"}),
    ]

    retriever = SimpleLexicalRetriever(docs)
    query = "лексический поиск BM25"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
