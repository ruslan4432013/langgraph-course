"""
Запуск полного RAG-агента и демонстрация работы.

Документация:
- Running Graphs: https://langchain-ai.github.io/langgraph/how-tos/stream-updates/
- Visualization: https://langchain-ai.github.io/langgraph/how-tos/visualization/
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

# ============================================
# Сборка графа (полный код)
# ============================================
print("📥 Инициализация RAG-агента...")

# Подготовка данных
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

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the question, "
    "grade it as relevant. Give a binary score 'yes' or 'no'."
)

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:\n ------- \n{question}\n ------- \n"
    "Formulate an improved question:"
)

GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \nContext: {context}"
)


class GradeDocuments(BaseModel):
    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


def generate_query_or_respond(state: MessagesState):
    response = response_model.bind_tools([retriever_tool]).invoke(state["messages"])
    return {"messages": [response]}


def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question"]:
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = grader_model.with_structured_output(GradeDocuments).invoke(
        [{"role": "user", "content": prompt}]
    )
    return "generate_answer" if response.binary_score == "yes" else "rewrite_question"


def rewrite_question(state: MessagesState):
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}


def generate_answer(state: MessagesState):
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}


# Сборка графа
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

print("✅ RAG-агент готов к работе!\n")

# ============================================
# Запуск агента
# ============================================
print("=" * 60)
print("🚀 ЗАПУСК AGENTIC RAG")
print("=" * 60)

question = "What does Lilian Weng say about types of reward hacking?"
print(f"\n❓ Вопрос: {question}\n")
print("-" * 60)

# Стриминг результатов
for chunk in graph.stream(
    {"messages": [{"role": "user", "content": question}]}
):
    for node, update in chunk.items():
        print(f"\n📍 Обновление от узла: {node}")
        print("-" * 40)
        update["messages"][-1].pretty_print()

print("\n" + "=" * 60)
print("✅ Выполнение завершено!")
print("=" * 60)

# ============================================
# Дополнительные тесты
# ============================================
print("\n\n🧪 ДОПОЛНИТЕЛЬНЫЙ ТЕСТ: Простой вопрос (без поиска)")
print("-" * 60)

for chunk in graph.stream(
    {"messages": [{"role": "user", "content": "Hello! What can you help me with?"}]}
):
    for node, update in chunk.items():
        print(f"\n📍 Узел: {node}")
        update["messages"][-1].pretty_print()