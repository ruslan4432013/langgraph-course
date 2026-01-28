# https://python.langchain.com/docs/tutorials/agentic_rag/
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from typing import List

class SimpleRetriever(BaseRetriever):
    docs: List[Document] = [Document(page_content="Пример документа")]

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.docs

llm = ChatOpenAI()
retriever = SimpleRetriever()
docs = retriever.invoke("query")

print(docs[0].page_content)
retriever_tool = create_retriever_tool(
    retriever,
    "search_docs",
    "Поиск релевантных документов"
)
tools = [retriever_tool]

prompt = ...  # ReAct prompt
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

print(agent_executor.invoke({"input": "Вопрос с retrieval?"}))