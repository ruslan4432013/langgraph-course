"""
Узел generate_query_or_respond — решает, вызывать retriever или отвечать напрямую.

Документация:
- LangGraph MessagesState: https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.MessagesState
- Chat Models: https://python.langchain.com/docs/concepts/chat_models/
- Tool Calling: https://python.langchain.com/docs/concepts/tool_calling/
"""

import os
import getpass

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Подготовка retriever tool
print("📥 Подготовка retriever tool...")
url = "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
docs = WebBaseLoader(url).load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs)
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()


@tool
def retrieve_blog_posts(query: str) -> str:
    """Search and return information about Lilian Weng blog posts."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


retriever_tool = retrieve_blog_posts

# Инициализация модели
response_model = init_chat_model("gpt-4o", temperature=0)


def generate_query_or_respond(state: MessagesState):
    """
    Вызывает модель для генерации ответа на основе текущего состояния.
    Решает — делать запрос через retriever или отвечать напрямую.
    """
    response = (
        response_model
        .bind_tools([retriever_tool])  # Привязка инструмента к модели
        .invoke(state["messages"])
    )
    return {"messages": [response]}


# Тестирование
print("\n🧪 Тест 1: Простое приветствие (не требует поиска)")
input1 = {"messages": [{"role": "user", "content": "hello!"}]}
result1 = generate_query_or_respond(input1)
result1["messages"][-1].pretty_print()

print("\n🧪 Тест 2: Вопрос о reward hacking (требует поиска)")
input2 = {
    "messages": [
        {
            "role": "user",
            "content": "What does Lilian Weng say about types of reward hacking?",
        }
    ]
}
result2 = generate_query_or_respond(input2)
result2["messages"][-1].pretty_print()

# Проверка наличия tool_calls
if result2["messages"][-1].tool_calls:
    print("\n✅ Модель решила вызвать инструмент retriever")
else:
    print("\n⚠️ Модель решила ответить напрямую")