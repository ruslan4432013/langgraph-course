from operator import add
from pprint import pprint
from typing import TypedDict, List, Annotated

from langgraph.constants import START, END

from lessons.module_4.subgraph.failure_analysis_subgraph import fa_builder
from lessons.module_4.subgraph.log_state import Log


from langgraph.graph import StateGraph

from lessons.module_4.subgraph.question_summarization_subgraph import qs_builder


class EntryGraphState(TypedDict):
    raw_logs: List[Log]
    cleaned_logs: List[Log]
    fa_summary: str # Будет генерироваться только в подграфе FA
    report: str # Будет генерироваться только в подграфе QS
    processed_logs: Annotated[List[int], add] # Будет генерироваться в ОБОИХ подграфах

def clean_logs(state):
    # Получаем логи
    raw_logs = state["raw_logs"]
    # Очистка данных: raw_logs -> docs
    cleaned_logs = raw_logs
    return {"cleaned_logs": cleaned_logs}

entry_builder = StateGraph(EntryGraphState)
entry_builder.add_node("clean_logs", clean_logs)
entry_builder.add_node("question_summarization", qs_builder.compile())
entry_builder.add_node("failure_analysis", fa_builder.compile())
entry_builder.add_edge(START, "clean_logs")
entry_builder.add_edge("clean_logs", "failure_analysis")
entry_builder.add_edge("clean_logs", "question_summarization")
entry_builder.add_edge("failure_analysis", END)
entry_builder.add_edge("question_summarization", END)
graph = entry_builder.compile()

if __name__ == '__main__':
    # Тестовые логи
    question_answer = Log(
        id="1",
        question="Как импортировать ChatOllama?",
        answer="Для импорта ChatOllama используйте: 'from langchain_community.chat_models import ChatOllama.'",
    )

    question_answer_feedback = Log(
        id="2",
        question="Как использовать хранилище векторов Chroma?",
        answer="Для использования Chroma определите: rag_chain = create_retrieval_chain(retriever, question_answer_chain).",
        grade=0,
        grader="Recall релевантности документа",
        feedback="Извлеченные документы обсуждают хранилища векторов в целом, но не Chroma конкретно",
    )

    raw_logs = [question_answer, question_answer_feedback]
    pprint(graph.invoke({"raw_logs": raw_logs}))

