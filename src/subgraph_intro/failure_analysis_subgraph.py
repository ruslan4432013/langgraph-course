from typing import TypedDict, List

from langgraph.graph import StateGraph, START, END

from src.subgraph_intro.log_state import Log


# Подграф анализа ошибок
class FailureAnalysisState(TypedDict):
    cleaned_logs: List[Log]
    failures: List[Log]
    fa_summary: str
    processed_logs: List[str]


class FailureAnalysisOutputState(TypedDict):
    fa_summary: str
    processed_logs: List[str]


def get_failures(state):
    """Получить логи, содержащие ошибки"""
    cleaned_logs = state["cleaned_logs"]
    failures = [log for log in cleaned_logs if "grade" in log]
    return {"failures": failures}


def generate_summary(state):
    """Сгенерировать сводку по ошибкам"""
    failures = state["failures"]
    # Добавить функцию: fa_summary = summarize(failures)
    fa_summary = "Низкое качество извлечения документации Chroma."
    return {"fa_summary": fa_summary,
            "processed_logs": [f"failure-analysis-on-log-{failure['id']}" for failure in failures]}


fa_builder = StateGraph(state_schema=FailureAnalysisState, output_schema=FailureAnalysisOutputState)
fa_builder.add_node("get_failures", get_failures)
fa_builder.add_node("generate_summary", generate_summary)
fa_builder.add_edge(START, "get_failures")
fa_builder.add_edge("get_failures", "generate_summary")
fa_builder.add_edge("generate_summary", END)
graph = fa_builder.compile()
