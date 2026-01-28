# https://python.langchain.com/docs/how_to/embeddings/

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
embedded_text = embeddings.embed_query("Пример текста для эмбеддинга")
print(len(embedded_text))