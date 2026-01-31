"""
Узел rewrite_question — переформулирует вопрос для улучшения поиска.

Документация:
- Messages: https://python.langchain.com/docs/concepts/messages/
- HumanMessage: https://python.langchain.com/api_reference/core/messages/langchain_core.messages.human.HumanMessage.html
"""

import os
import getpass

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, convert_to_messages
from langgraph.graph import MessagesState

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Промпт для переформулирования
REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)

# Модель для переформулирования
response_model = init_chat_model("gpt-4o", temperature=0)


def rewrite_question(state: MessagesState):
    """
    Переформулирует исходный вопрос пользователя для улучшения результатов поиска.
    """
    messages = state["messages"]
    question = messages[0].content  # Исходный вопрос пользователя

    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])

    # Возвращаем новое сообщение пользователя с переформулированным вопросом
    return {"messages": [HumanMessage(content=response.content)]}


# Тестирование
print("🧪 Тестирование переформулирования вопроса")

input_state = {
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
        {"role": "tool", "content": "meow", "tool_call_id": "1"},  # Нерелевантный результат
    ])
}

print(f"\n📝 Исходный вопрос:")
print(f"   {input_state['messages'][0].content}")

response = rewrite_question(input_state)

print(f"\n✨ Переформулированный вопрос:")
print(f"   {response['messages'][-1].content}")