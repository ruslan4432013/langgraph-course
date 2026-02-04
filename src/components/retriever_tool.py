from langchain.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from src.components.process_documents import doc_splits
from src.settings import settings

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, base_url='https://api.proxyapi.ru/openai/v1')
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


@tool
def retrieve_blog_posts(query: str) -> str:
    """Поиск и получение информации из блогов Лилиан Венг. Запрос должен быть на английском языке."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


retriever_tool = retrieve_blog_posts

if __name__ == "__main__":
    result = retriever_tool.invoke({"query": "types of reward hacking"})
    print(result)
