from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.retrieve import context
from src.settings import settings

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url='https://api.proxyapi.ru/openai/v1',
    model="gpt-5",
)

prompt_template = ChatPromptTemplate([
    ("system", "Ты — полезный помощник. Используй следующий контекст, чтобы ответить на вопрос. "
               "Если ответа нет в контексте — скажи об этом.\n\nКонтекст:\n {context}"),
    ("user", "{question}")
])

chain = prompt_template | llm

question = "Как общается Зир'фан?"

response = chain.invoke({
    "question": question,
    "context": context,
})
print(response.content)
