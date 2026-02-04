from typing import Literal

from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

from src.settings import settings

GRADE_PROMPT = (
    "Ты — эксперт, оценивающий релевантность извлеченного документа вопросу пользователя. \n "
    "Вот извлеченный документ: \n\n {context} \n\n"
    "Вот вопрос пользователя: {question} \n"
    "Если документ содержит ключевые слова или семантический смысл, связанный с вопросом пользователя, оцени его как релевантный. \n"
    "Если документ перечисляет только разделы статьи (например, «Hacking RL Environment», «Hacking RLHF of LLMs», «Hacking the Training Process», «Hacking the Evaluator»), но нет её содержимого или утверждений, ответь 'no' \n"
    "Дай бинарную оценку 'yes' (да) или 'no' (нет), чтобы указать, релевантен ли документ вопросу."
)


class GradeDocuments(BaseModel):
    """Оценка документов с использованием бинарного балла для проверки релевантности."""

    binary_score: str = Field(
        description="Оценка релевантности: 'yes', если документ релевантен, или 'no', если нет"
    )


grader_model = init_chat_model(
    "gpt-5.2",
    temperature=0,
    api_key=settings.OPENAI_API_KEY,
    base_url='https://api.proxyapi.ru/openai/v1'
)


def grade_documents(
        state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """Определить, релевантны ли извлеченные документы вопросу."""
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments).invoke(
            [{"role": "user", "content": prompt}]
        )
    )
    score = response.binary_score

    if score == "yes":
        return "generate_answer"

    return "rewrite_question"


if __name__ == "__main__":
    from langchain_core.messages import convert_to_messages

    input_value = {
        "messages": convert_to_messages(
            [
                {
                    "role": "user",
                    "content": "Что Лилиан Венг говорит о типах взлома вознаграждения?",
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
                {"role": "tool", "content": "meow", "tool_call_id": "1"},
            ]
        )
    }
    result_1 = grade_documents(input_value)
    print(f"{result_1=}")

    input_value_2 = {
        "messages": convert_to_messages(
            [
                {
                    "role": "user",
                    "content": "Что Лилиан Венг говорит о типах взлома вознаграждения?",
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
            ]
        )
    }
    result_2 = grade_documents(input_value_2)

    print(f"{result_2=}")
