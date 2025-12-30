from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class DummyRetrieverA(BaseRetriever):
    def __init__(self, documents):
        self._documents = documents

    def _get_relevant_documents(self, query):
        # Возвращаем первый документ
        return [self._documents[0]]


class DummyRetrieverB(BaseRetriever):
    def __init__(self, documents):
        self._documents = documents

    def _get_relevant_documents(self, query):
        # Возвращаем последний документ
        return [self._documents[-1]]


class SimpleEnsembleRetriever(BaseRetriever):
    def __init__(self, retrievers, weights):
        super().__init__()
        self._retrievers = retrievers
        self._weights = weights

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun):
        score_map = {}
        for retriever, weight in zip(self._retrievers, self._weights):
            docs = retriever._get_relevant_documents(query)
            for rank, doc in enumerate(docs, start=1):
                # Имитация Reciprocal Rank Fusion
                key = id(doc)
                score = weight * (1.0 / (rank + 1))
                if key not in score_map:
                    score_map[key] = {"score": 0.0, "doc": doc}
                score_map[key]["score"] += score

        scored_docs = list(score_map.values())
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return [item["doc"] for item in scored_docs]


if __name__ == "__main__":
    docs = [
        Document(page_content="Документ A", metadata={"id": "A"}),
        Document(page_content="Документ B", metadata={"id": "B"}),
        Document(page_content="Документ C", metadata={"id": "C"}),
    ]

    retriever_a = DummyRetrieverA(docs)
    retriever_b = DummyRetrieverB(docs)

    ensemble_retriever = SimpleEnsembleRetriever(
        retrievers=[retriever_a, retriever_b],
        weights=[0.5, 0.9],
    )

    query = "любой запрос"
    result_docs = ensemble_retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
