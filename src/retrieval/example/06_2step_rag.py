# https://python.langchain.com/docs/tutorials/rag/

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("Ответь на вопрос: {question}\nКонтекст: {context}")
retriever = ...  # Из предыдущего примера

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("Вопрос?"))