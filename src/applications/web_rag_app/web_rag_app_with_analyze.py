from typing import Literal

import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import Annotated, List, TypedDict

from src.components.llm_model import llm
from src.components.vector_store_client import vector_store

# Загружаем содержимое блога и разбиваем на части
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Обновляем метаданные (в иллюстрационных целях)
total_documents = len(all_splits)
third = total_documents // 3

for i, document in enumerate(all_splits):
    if i < third:
        document.metadata["section"] = "beginning"
    elif i < 2 * third:
        document.metadata["section"] = "middle"
    else:
        document.metadata["section"] = "end"

# Индексируем фрагменты
_ = vector_store.add_documents(all_splits)


# Определяем схему для поиска
class Search(TypedDict):
    """Поисковый запрос."""

    query: Annotated[str, ..., "Поисковый запрос для выполнения."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Секция для запроса.",
    ]


# Определяем промпт для ответа на вопросы
prompt = hub.pull("rlm/rag-prompt")


# Определяем состояние приложения
class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str


class InputState(TypedDict):
    question: str


def analyze_query(state: State):
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    return {"query": query}


def retrieve(state: State):
    query = state["query"]
    retrieved_docs = vector_store.similarity_search(
        query["query"],
        filter={"section": query["section"]},
    )
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


graph_builder = StateGraph(State, input_schema=InputState).add_sequence([analyze_query, retrieve, generate])
graph_builder.add_edge(START, "analyze_query")
graph = graph_builder.compile()
