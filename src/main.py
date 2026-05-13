from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.llm.openrouter_api import llm_openai


# 1. Определяем состояние графа
class State(TypedDict):
    value: int


# 2. Определяем узлы (обычные Python-функции)
def add(state: State) -> State:
    result = llm_openai.invoke(f"add {state['value']} to 10")
    print(result.content)
    return {
        "value": state["value"] + 2,
    }


# 3. Создаём граф
graph = StateGraph(State)

graph.add_node('add', add)

# 5. Соединяем узлы рёбрами
graph.add_edge(START, "add")
graph.add_edge("add", END)

# 6. Компилируем граф
app = graph.compile()


if __name__ == "__main__":
    # 7. Запускаем
    result = app.invoke({"value": 8})

    print(result)
