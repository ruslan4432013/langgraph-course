from langchain_openai import OpenAIEmbeddings

from ..settings import settings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large",
                              api_key=settings.OPENAI_API_KEY,
                              base_url='https://api.proxyapi.ru/openai/v1')
