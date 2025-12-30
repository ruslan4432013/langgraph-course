from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class MultiVectorIndex:
    """
    Инфраструктура для хранения документов и их множественных векторных представлений.
    Позволяет сопоставлять несколько векторов (представлений) с одним и тем же исходным документом.
    """

    def __init__(self):
        """
        Инициализирует пустое хранилище векторов и документов.
        """
        # key: vector_id, value: {"doc_id": ..., "representation": ...}
        self.vectors = {}
        self.doc_store = {}

    def add_document_with_representations(self, doc_id, document, representations):
        """
        Добавляет документ в хранилище вместе с набором его представлений.

        Args:
            doc_id (str): Уникальный идентификатор документа.
            document (Document): Объект документа LangChain.
            representations (list[str]): Список текстовых представлений (резюме, вопросы и т.д.) для индексации.
        """
        self.doc_store[doc_id] = document
        for i, rep in enumerate(representations):
            vector_id = f"{doc_id}_v{i}"
            self.vectors[vector_id] = {"doc_id": doc_id, "representation": rep}

    def similarity_search_doc_ids(self, query, k=2):
        """
        Выполняет поиск наиболее похожих представлений и возвращает соответствующие ID документов.

        Args:
            query (str): Поисковый запрос.
            k (int): Количество уникальных документов для возврата.

        Returns:
            list[str]: Список ID найденных документов.
        """
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
    """
    Ретривер, который использует несколько векторов для поиска одного документа.
    Это полезно, когда один документ может иметь разные формы представления (например, краткое изложение или частые вопросы).
    """

    def __init__(self, index):
        """
        Инициализирует ретривер с заданным индексом.

        Args:
            index (MultiVectorIndex): Индекс, содержащий документы и их представления.
        """
        super().__init__()
        self._index = index

    def _get_relevant_documents(self, query):
        """
        Внутренний метод для получения релевантных документов по запросу.

        Args:
            query (str): Поисковый запрос.

        Returns:
            list[Document]: Список найденных документов.
        """
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
