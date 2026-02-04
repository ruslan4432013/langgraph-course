from langchain_core.messages import convert_to_messages
from langgraph.graph import MessagesState

from src.components.generate_query import response_model

GENERATE_PROMPT = (
    "Ты — помощник по ответам на вопросы. "
    "Используй следующие фрагменты извлеченного контекста, чтобы ответить на вопрос. "
    "Если ты не знаешь ответа, просто скажи, что не знаешь. "
    "Используй максимум три предложения и старайся отвечать кратко.\n"
    "Вопрос: {question} \n"
    "Контекст: {context}"
)


def generate_answer(state: MessagesState):
    """Сгенерировать ответ."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}


if __name__ == "__main__":
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
                {
                    "role": "tool",
                    "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
                    "tool_call_id": "1",
                },
            ]
        )
    }

    response = generate_answer(input_value)
    response["messages"][-1].pretty_print()
