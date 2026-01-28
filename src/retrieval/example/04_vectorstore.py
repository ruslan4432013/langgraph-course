# https://python.langchain.com/docs/integrations/vectorstores/

from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
texts = ["Текст 1", "Текст 2"]
vectorstore = InMemoryVectorStore.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()
docs = retriever.get_relevant_documents("Текст 1")
print(docs[0].page_content)