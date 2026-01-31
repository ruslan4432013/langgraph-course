"""
Визуализация графа RAG-агента.

Документация:
- Visualization: https://langchain-ai.github.io/langgraph/how-tos/visualization/
- Mermaid: https://mermaid.js.org/
"""

import os
import getpass
from typing import Literal

from pydantic import BaseModel, Field
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Минимальная сборка графа для визуализации
print("📥 Сборка графа для визуализации...")

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
response_model = init_chat_model("gpt-4o", temperature=0)
grader_model = init_chat_model("gpt-4o", temperature=0)


class GradeDocuments(BaseModel):
    binary_score: str = Field(description="'yes' or 'no'")


def generate_query_or_respond(state: MessagesState):
    response = response_model.bind_tools([retriever_tool]).invoke(state["messages"])
    return {"messages": [response]}


def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question"]:
    return "generate_answer"  # Упрощённо для визуализации


def rewrite_question(state: MessagesState):
    return {"messages": [HumanMessage(content="rewritten question")]}


def generate_answer(state: MessagesState):
    return {"messages": []}


# Сборка
workflow = StateGraph(MessagesState)
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

workflow.add_edge(START, "generate_query_or_respond")
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {"tools": "retrieve", END: END},
)
workflow.add_conditional_edges("retrieve", grade_documents)
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

graph = workflow.compile()

# ============================================
# Визуализация
# ============================================
print("\n📊 Визуализация графа")
print("=" * 60)

# Получение Mermaid-диаграммы
mermaid_code = graph.get_graph().draw_mermaid()
print("\n🔷 Mermaid-код диаграммы:")
print("-" * 40)
print(mermaid_code)

# Сохранение в файл
with open("graph_diagram.md", "w") as f:
    f.write("```mermaid\n")
    f.write(mermaid_code)
    f.write("\n```")
print("\n✅ Диаграмма сохранена в graph_diagram.md")

# Для Jupyter Notebook - отображение PNG
try:
    from IPython.display import Image, display

    png_data = graph.get_graph().draw_mermaid_png()
    with open("graph_diagram.png", "wb") as f:
        f.write(png_data)
    print("✅ PNG-изображение сохранено в graph_diagram.png")

    # Отображение в notebook
    # display(Image(png_data))
except ImportError:
    print("ℹ️  IPython не установлен. Для отображения PNG используйте Jupyter Notebook.")
except Exception as e:
    print(f"⚠️  Не удалось создать PNG: {e}")

print("\n📋 Структура графа:")
print("-" * 40)
graph_structure = graph.get_graph()
print(f"   Узлы: {list(graph_structure.nodes.keys())}")
print(f"   Количество рёбер: {len(graph_structure.edges)}")