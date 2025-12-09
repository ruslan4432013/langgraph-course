from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class MultiVectorIndex:
    def __init__(self):
        # key: vector_id, value: {"doc_id": ..., "representation": ...}
        self.vectors = {}
        self.doc_store = {}

    def add_document_with_representations(self, doc_id, document, representations):
        self.doc_store[doc_id] = document
        for i, rep in enumerate(representations):
            vector_id = f"{doc_id}_v{i}"
            self.vectors[vector_id] = {"doc_id": doc_id, "representation": rep}

    def similarity_search_doc_ids(self, query, k=2):
        # Заглушка: вернуть первые k doc_id на основе «похожести» по длине строки
        scored = []
        for vector_id, payload in self.vectors.items():
            rep = payload["representation"]
            score = -abs(len(rep) - len(query))  # псевдо-оценка
            scored.append((score, payload["doc_id"]))
        scored.sort(key=lambda x: x[0], reverse=True)
        doc_ids = []
        for _, doc_id in scored:
            if doc_id not in doc_ids:
                doc_ids.append(doc_id)
            if len(doc_ids) >= k:
                break
        return doc_ids


class MultiVectorRetriever(BaseRetriever):
    def __init__(self, index):
        self._index = index

    def _get_relevant_documents(self, query):
        doc_ids = self._index.similarity_search_doc_ids(query, k=2)
        return [self._index.doc_store[doc_id] for doc_id in doc_ids]


if __name__ == "__main__":
    index = MultiVectorIndex()

    doc = Document(
        page_content="Документ о мультивекторном ретривере.",
        metadata={"id": "doc1"},
    )

    # Разные представления одного документа: краткое резюме и гипотетический вопрос
    representations = [
        "мультивекторный ретривер, несколько векторов на документ",
        "как работает multi vector retriever?",
    ]

    index.add_document_with_representations(
        doc_id="doc1",
        document=doc,
        representations=representations,
    )

    retriever = MultiVectorRetriever(index)

    query = "несколько векторов на один документ"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("НАЙДЕННЫЙ ДОКУМЕНТ:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
