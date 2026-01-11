import operator
from typing import Annotated

from langchain_openai import ChatOpenAI
from langgraph.types import Send
from pydantic import BaseModel
from typing_extensions import TypedDict

from src.settings import settings

subjects_prompt = """Сгенерируй список из 3 подтем, которые все относятся к общей теме: {topic}."""

joke_prompt = """Сгенерируй шутку про {subject}"""

best_joke_prompt = """Ниже находится множество шуток про {topic}. Выберите лучшую! Верните ID лучшей шутки, начиная с 0 как ID для первой шутки. Шутки: \n\n  {jokes}"""

model = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)


class Subjects(BaseModel):
    subjects: list[str]


class BestJoke(BaseModel):
    id: int


class OverallState(TypedDict):
    topic: str
    subjects: list
    jokes: Annotated[list, operator.add]
    best_selected_joke: str


# Генерация тем для шуток.
def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}


def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


class JokeState(TypedDict):
    subject: str


class Joke(BaseModel):
    joke: str


def generate_joke(state: JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Joke).invoke(prompt)
    return {"jokes": [response.joke]}


def best_joke(state: OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"], jokes=jokes)
    response = model.with_structured_output(BestJoke).invoke(prompt)
    return {"best_selected_joke": state["jokes"][response.id]}


from langgraph.graph import END, StateGraph, START


class InputState(TypedDict):
    topic: str


# Конструируем граф: здесь мы собираем всё вместе, чтобы построить наш граф
graph = StateGraph(OverallState, input_schema=InputState)
graph.add_node("generate_topics", generate_topics)
graph.add_node("generate_joke", generate_joke)
graph.add_node("best_joke", best_joke)
graph.add_edge(START, "generate_topics")
graph.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
graph.add_edge("generate_joke", "best_joke")
graph.add_edge("best_joke", END)

# Компилируем граф
app = graph.compile()

# Вызываем граф: здесь мы вызываем его, чтобы сгенерировать список шуток
if __name__ == '__main__':
    for s in app.stream({"topic": "Животные"}):
        print(s)
