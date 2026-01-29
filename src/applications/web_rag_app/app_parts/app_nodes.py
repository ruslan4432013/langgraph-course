from langchain_core.messages import AIMessage

from src.applications.web_rag_app.app_parts.app_states import State, Search
from src.applications.web_rag_app.app_parts.get_rag_prompt import prompt
from src.components.llm_model import llm
from src.components.vector_store_client import vector_store


def analyze_query(state: State):
    structured_llm = llm.with_structured_output(Search)
    query = structured_llm.invoke(state["question"])
    return {"query": query}


def retrieve(state: State):
    query = state["query"]
    retrieved_docs = vector_store.similarity_search(
        query["query"],
        filter=lambda doc: doc.metadata.get("section") == query["section"],
    )
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response: AIMessage = llm.invoke(messages)
    return {"answer": response.content}
