"""
Узел generate_answer — генерирует финальный ответ на основе контекста.

Документация:
- RAG: https://python.langchain.com/docs/concepts/rag/
- Prompts: https://python.langchain.com/docs/concepts/prompts/
"""

import os
import getpass

from langchain.chat_models import init_chat_model
from langchain_core.messages import convert_to_messages
from langgraph.graph import MessagesState

# Настройка
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY:")

# Промпт для генерации ответа
GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context}"
)

# Модель для генерации ответа
response_model = init_chat_model("gpt-4o", temperature=0)


def generate_answer(state: MessagesState):
    """
    Генерирует финальный ответ на основе вопроса и извлечённого контекста.
    """
    question = state["messages"][0].content  # Исходный вопрос
    context = state["messages"][-1].content  # Контекст из retriever (ToolMessage)

    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])

    return {"messages": [response]}


# Тестирование
print("🧪 Тестирование генерации ответа")

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
        {
            "role": "tool",
            "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
            "tool_call_id": "1",
        },
    ])
}

print(f"\n❓ Вопрос: {input_state['messages'][0].content}")
print(f"\n📚 Контекст: {input_state['messages'][-1].content}")

response = generate_answer(input_state)

print(f"\n💬 Сгенерированный ответ:")
response["messages"][-1].pretty_print()