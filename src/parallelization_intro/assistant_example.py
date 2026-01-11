import operator
import os
from typing import TypedDict, Annotated

from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.settings import settings

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

llm = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)


class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]


class InputState(TypedDict):
    question: str


def search_web(state: State):
    """Получить документы из веб-поиска"""
    # Поиск
    tavily_search = TavilySearch(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)
    search_docs = tavily_search.invoke(state['question'])
    docs = search_docs['results']
    # Форматирование
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in docs
        ]
    )
    print(f'[search_web] {formatted_search_docs=}')
    return {"context": [formatted_search_docs]}


def search_wikipedia(state: State):
    """Получить документы из Wikipedia"""
    # Поиск
    search_docs = WikipediaLoader(query=state['question'], load_max_docs=2, lang='ru').load()
    # Форматирование
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    print(f'[search_wikipedia] {formatted_search_docs=}')
    return {"context": [formatted_search_docs]}


def generate_answer(state):
    """Узел для ответа на вопрос"""
    # Получить состояние
    context = state["context"]
    question = state["question"]

    # Шаблон
    answer_template = """Ответьте на вопрос {question}, используя этот контекст: {context}"""
    answer_instructions = answer_template.format(question=question, context=context)

    # Ответ
    answer = llm.invoke([SystemMessage(content=answer_instructions)] + [HumanMessage(content="Ответьте на вопрос.")])

    # Добавить в состояние
    return {"answer": answer.content}


# Добавить узлы
builder = StateGraph(State, input_schema=InputState)

# Инициализировать каждый узел с node_secret
builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

# Поток
builder.add_edge(START, "search_wikipedia")
builder.add_edge(START, "search_web")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"question": "Что такое Nvidia?"})
    print(result['answer'])
