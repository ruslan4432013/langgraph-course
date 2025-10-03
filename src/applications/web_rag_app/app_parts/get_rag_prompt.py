from langchain import hub
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import ChatPromptValue

prompt = hub.pull("rlm/rag-prompt")

chat_prompt_value: ChatPromptValue = prompt.invoke(
    {"context": "(Контекст будем вставлять здесь)", "question": "(Вопрос вставляем здесь)"}
)

chat_prompt_messages: list[BaseMessage] = chat_prompt_value.to_messages()

print(chat_prompt_messages[0].content)
