from typing import Literal

from langchain_core.documents import Document
from typing_extensions import Annotated
from typing_extensions import List, TypedDict


class Search(TypedDict):
    """Search query."""

    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Section to query.",
    ]


class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str


class InputState(TypedDict):
    question: str
