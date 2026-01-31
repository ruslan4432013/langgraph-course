"""
Условное ребро grade_documents — определяет релевантность документов.

Документация:
- Structured Output: https://python.langchain.com/docs/concepts/structured_outputs/
- Conditional Edges: https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges
- Pydantic: https://docs.pydantic.dev/latest/
"""

import os
import getpass
from typing import Literal

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import convert_to_messages
from langgraph.graph import MessagesState

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Промпт для оценки документов
GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \n "
    "Here is the retrieved document: \n\n {context} \n\n"
    "Here is the user question: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, "
    "grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant "
    "to the question."
)


# Pydantic-схема для структурированного вывода
class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )


# Модель для оценки
grader_model = init_chat_model("gpt-4o", temperature=0)


def grade_documents(
        state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """
    Определяет релевантность документов вопросу.
    Возвращает имя следующего узла: 'generate_answer' или 'rewrite_question'.
    """
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)

    # Использование structured output для получения оценки
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


# Тестирование
print("🧪 Тест 1: Нерелевантный документ")
input_irrelevant = {
    "messages": convert_to_messages([
        {
            "role": "user",
            "content": "What does Lilian Weng say about types of reward hacking?",
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "1",
                    "name": "retrieve_blog_posts",
                    "args": {"query": "types of reward hacking"},
                }
            ],
        },
        {"role": "tool", "content": "meow", "tool_call_id": "1"},  # Нерелевантный контент
    ])
}
result1 = grade_documents(input_irrelevant)
print(f"   Результат: {result1}")
print(f"   ✅ Ожидается 'rewrite_question'" if result1 == "rewrite_question" else "   ⚠️ Неожиданный результат")

print("\n🧪 Тест 2: Релевантный документ")
input_relevant = {
    "messages": convert_to_messages([
        {
            "role": "user",
            "content": "What does Lilian Weng say about types of reward hacking?",
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "1",
                    "name": "retrieve_blog_posts",
                    "args": {"query": "types of reward hacking"},
                }
            ],
        },
        {
            "role": "tool",
            "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
            "tool_call_id": "1",
        },
    ])
}
result2 = grade_documents(input_relevant)
print(f"   Результат: {result2}")
print(f"   ✅ Ожидается 'generate_answer'" if result2 == "generate_answer" else "   ⚠️ Неожиданный результат")