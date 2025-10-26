from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from src.settings import settings

text_splitter = SemanticChunker(
    OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, base_url='https://api.proxyapi.ru/openai/v1')
)

with open("./rag_article.txt", "r") as f:
    text = f.read()

docs = text_splitter.create_documents([text])

for i, doc in enumerate(docs, start=1):
    print('-' * 50)
    print(f"Chunk: {i}")
    print(doc.page_content)
