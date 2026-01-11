# Подграф суммаризации
from typing import List, TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.subgraph_intro.log_state import Log


class QuestionSummarizationState(TypedDict):
    cleaned_logs: List[Log]
    qs_summary: str
    report: str
    processed_logs: List[str]


class QuestionSummarizationOutputState(TypedDict):
    report: str
    processed_logs: List[str]


def generate_summary(state):
    cleaned_logs = state["cleaned_logs"]
    # Добавить функцию: summary = summarize(generate_summary)
    summary = "Вопросы касались использования ChatOllama и хранилища векторов Chroma."
    return {"qs_summary": summary, "processed_logs": [f"summary-on-log-{log['id']}" for log in cleaned_logs]}


def send_to_slack(state):
    qs_summary = state["qs_summary"]
    # Добавить функцию: report = report_generation(qs_summary)
    report = "foo bar baz"
    return {"report": report}


qs_builder = StateGraph(QuestionSummarizationState, output_schema=QuestionSummarizationOutputState)
qs_builder.add_node("generate_summary", generate_summary)
qs_builder.add_node("send_to_slack", send_to_slack)
qs_builder.add_edge(START, "generate_summary")
qs_builder.add_edge("generate_summary", "send_to_slack")
qs_builder.add_edge("send_to_slack", END)
graph = qs_builder.compile()
