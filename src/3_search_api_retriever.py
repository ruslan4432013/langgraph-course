from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def fake_search_api(query):
    # Имитируем внешний поисковый API, который возвращает «сырые» результаты
    return [
        {"title": "Ретриверы в LangChain", "url": "https://example.com/retrievers"},
        {"title": "Поиск по Wikipedia", "url": "https://example.com/wikipedia"},
    ]


class SearchApiRetriever(BaseRetriever):
    def _get_relevant_documents(self, query):
        raw_results = fake_search_api(query)
        docs = []
        for item in raw_results:
            text = f"{item['title']} ({item['url']})"
            docs.append(Document(page_content=text, metadata=item))
        return docs


if __name__ == "__main__":
    retriever = SearchApiRetriever()
    query = "ретриверы langchain"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
