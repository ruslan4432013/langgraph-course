from langchain_core.tools import tool

from src.components.vector_store_client import vector_store


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """
    Извлечение информации соответствующей запросу.
    # Используй английский язык для запроса
    """
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
