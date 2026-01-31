"""
agentic_rag.py

Построение кастомного RAG-агента с LangGraph.
Демонстрирует:
- Загрузку и предобработку документов
- Индексацию документов для семантического поиска
- Создание инструмента-retriever
- Построение агентной RAG-системы с оценкой релевантности и переформулированием вопросов
"""

import getpass
import os
from typing import Literal

from pydantic import BaseModel, Field

# LangChain imports
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage, convert_to_messages
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# LangGraph imports
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


# ==============================================================================
# 0. SETUP - Настройка окружения
# ==============================================================================

def _set_env(key: str):
    """Установка переменной окружения, если она не задана."""
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")


_set_env("OPENAI_API_KEY")

# ==============================================================================
# 1. ПРЕДВАРИТЕЛЬНАЯ ОБРАБОТКА ДОКУМЕНТОВ
# ==============================================================================

print("=" * 60)
print("1. Загрузка и обработка документов...")
print("=" * 60)

# Загрузка документов из блога Лилиан Венг
urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

docs = [WebBaseLoader(url).load() for url in urls]
print(f"Загружено {len(docs)} документов")

# Преобразование в плоский список
docs_list = [item for sublist in docs for item in sublist]

# Разбиение документов на чанки
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
print(f"Документы разбиты на {len(doc_splits)} фрагментов")

# Пример первого фрагмента
print(f"\nПример фрагмента:\n{doc_splits[0].page_content.strip()[:200]}...")

# ==============================================================================
# 2. СОЗДАНИЕ ИНСТРУМЕНТА RETRIEVER
# ==============================================================================

print("\n" + "=" * 60)
print("2. Создание векторного хранилища и инструмента retriever...")
print("=" * 60)

# Индексация документов в векторное хранилище
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
print("Векторное хранилище создано")


@tool
def retrieve_blog_posts(query: str) -> str:
    """Search and return information about Lilian Weng blog posts."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


retriever_tool = retrieve_blog_posts
print("Инструмент retriever создан")

# Тест инструмента
print("\nТест retriever:")
print(retriever_tool.invoke({"query": "types of reward hacking"})[:300] + "...")

# ==============================================================================
# 3. ОПРЕДЕЛЕНИЕ УЗЛОВ И РЁБЕР ГРАФА
# ==============================================================================

print("\n" + "=" * 60)
print("3. Определение узлов и рёбер графа...")
print("=" * 60)

# Инициализация моделей
response_model = init_chat_model("gpt-4o", temperature=0)
grader_model = init_chat_model("gpt-4o", temperature=0)

# --- Промпты ---

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, "
    "grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant "
    "to the question."
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


# --- Схема для структурированного вывода ---

class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""
    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


# --- Узел 1: Генерация запроса или ответа ---

def generate_query_or_respond(state: MessagesState):
    """
    Вызывает LLM для генерации ответа на основе текущего состояния.
    Решает — делать ли запрос через retriever или ответить напрямую.
    """
    response = (
        response_model
        .bind_tools([retriever_tool])
        .invoke(state["messages"])
    )
    return {"messages": [response]}


# --- Условное ребро: Оценка документов ---

def grade_documents(
        state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """
    Определяет, релевантны ли извлечённые документы вопросу.
    Возвращает имя следующего узла.
    """
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments)
        .invoke([{"role": "user", "content": prompt}])
    )
    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"


# --- Узел 2: Переформулирование вопроса ---

def rewrite_question(state: MessagesState):
    """Переписывает исходный вопрос пользователя для улучшения поиска."""
    messages = state["messages"]
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}


# --- Узел 3: Генерация ответа ---

def generate_answer(state: MessagesState):
    """Генерирует финальный ответ на основе вопроса и извлечённого контекста."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}


print("Все узлы и рёбра определены")

# ==============================================================================
# 4. СБОРКА ГРАФА
# ==============================================================================

print("\n" + "=" * 60)
print("4. Сборка графа...")
print("=" * 60)

workflow = StateGraph(MessagesState)

# Добавление узлов
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

# Добавление рёбер
workflow.add_edge(START, "generate_query_or_respond")

# Условное ребро: решение о необходимости поиска
workflow.add_conditional_edges(
    "generate_query_or_respond",
    # Оценка решения LLM (вызвать retriever_tool или ответить пользователю)
    tools_condition,
    {
        "tools": "retrieve",
        END: END,
    },
)

# Условное ребро после извлечения: оценка релевантности документов
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,
)

workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

# Компиляция графа
graph = workflow.compile()

print("Граф успешно собран и скомпилирован!")

# Опциональная визуализация (требует IPython)
try:
    from IPython.display import Image, display

    display(Image(graph.get_graph().draw_mermaid_png()))
    print("Визуализация графа отображена")
except ImportError:
    print("Визуализация недоступна (требуется IPython)")
except Exception as e:
    print(f"Ошибка визуализации: {e}")

# ==============================================================================
# 5. ЗАПУСК AGENTIC RAG
# ==============================================================================

print("\n" + "=" * 60)
print("5. Запуск Agentic RAG...")
print("=" * 60)


def run_agentic_rag(question: str):
    """Запускает RAG-агента с заданным вопросом."""
    print(f"\n{'─' * 40}")
    print(f"Вопрос: {question}")
    print("─" * 40)

    for chunk in graph.stream(
            {"messages": [{"role": "user", "content": question}]}
    ):
        for node, update in chunk.items():
            print(f"\n► Узел: {node}")
            update["messages"][-1].pretty_print()


# Тест 1: Вопрос, требующий поиска
run_agentic_rag("What does Lilian Weng say about types of reward hacking?")

# Тест 2: Простое приветствие (без поиска)
run_agentic_rag("Hello! How are you?")

# Тест 3: Вопрос о галлюцинациях
run_agentic_rag("What are the main causes of LLM hallucinations according to the blog?")

# ==============================================================================
# ИНТЕРАКТИВНЫЙ РЕЖИМ (опционально)
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Интерактивный режим (введите 'exit' для выхода)")
    print("=" * 60)

    while True:
        try:
            user_question = input("\nВаш вопрос: ").strip()
            if user_question.lower() in ("exit", "quit", "q"):
                print("До свидания!")
                break
            if user_question:
                run_agentic_rag(user_question)
        except KeyboardInterrupt:
            print("\nПрервано пользователем")
            break