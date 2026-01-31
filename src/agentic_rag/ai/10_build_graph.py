"""
Сборка полного графа RAG-агента с использованием LangGraph.

Документация:
- StateGraph: https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.StateGraph
- ToolNode: https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.ToolNode
- tools_condition: https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.tools_condition
- Edges: https://langchain-ai.github.io/langgraph/concepts/low_level/#edges
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
# 1. Подготовка retriever tool
# ============================================
print("📥 Подготовка компонентов...")
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

# ============================================
# 2. Определение моделей и промптов
# ============================================
response_model = init_chat_model("gpt-4o", temperature=0)
grader_model = init_chat_model("gpt-4o", temperature=0)

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, "
    "grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant."
)

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)

GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context}"
)


class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""
    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


# ============================================
# 3. Определение узлов (nodes)
# ============================================
def generate_query_or_respond(state: MessagesState):
    """Решает: вызывать retriever или отвечать напрямую."""
    response = (
        response_model
        .bind_tools([retriever_tool])
        .invoke(state["messages"])
    )
    return {"messages": [response]}


def grade_documents(
    state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """Оценивает релевантность документов."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments)
        .invoke([{"role": "user", "content": prompt}])
    )
    if response.binary_score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"


def rewrite_question(state: MessagesState):
    """Переформулирует вопрос."""
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}


def generate_answer(state: MessagesState):
    """Генерирует финальный ответ."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}


# ============================================
# 4. Сборка графа
# ============================================
print("🔨 Сборка графа...")

workflow = StateGraph(MessagesState)

# Добавление узлов
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

# Добавление рёбер
workflow.add_edge(START, "generate_query_or_respond")

# Условное ребро: retriever или конец
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,  # Проверяет наличие tool_calls
    {
        "tools": "retrieve",  # Если есть tool_calls -> retrieve
        END: END,             # Иначе -> завершение
    },
)

# Условное ребро после retrieve: оценка документов
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
    # grade_documents возвращает "generate_answer" или "rewrite_question"
)

# Финальные рёбра
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

# Компиляция графа
graph = workflow.compile()

print("✅ Граф собран и скомпилирован!")

# Вывод структуры графа
print("\n📊 Структура графа:")
print(f"   Узлы: {list(graph.get_graph().nodes.keys())}")