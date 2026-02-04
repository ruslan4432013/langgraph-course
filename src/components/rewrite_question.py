from langchain.messages import HumanMessage
from langchain_core.messages import convert_to_messages
from langgraph.graph import MessagesState

from src.components.generate_query import response_model

REWRITE_PROMPT = (
    "Посмотри на входные данные и попытайся проанализировать базовое семантическое намерение / значение.\n"
    "Вот исходный вопрос:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Сформулируй улучшенный вопрос:"
)


def rewrite_question(state: MessagesState):
    """Переформулировать исходный вопрос пользователя."""
    messages = state["messages"]
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [HumanMessage(content=response.content)]}


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
                {"role": "tool", "content": "meow", "tool_call_id": "1"},
            ]
        )
    }

    response = rewrite_question(input_value)
    print(response["messages"][-1].content)
