import time

from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings

from src.settings import settings

# Базовая ("подлежащая") модель эмбеддингов
underlying_embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)  # например, OpenAIEmbeddings(), HuggingFaceEmbeddings() и т.п.

# Хранилище, которое сохраняет эмбеддинги на локальный диск
# Не предназначено для продакшена, но удобно для локальных экспериментов
store = LocalFileStore("./cache_1/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    # Эмбеддер, который используется для встраивания (создания эмбеддингов).
    underlying_embeddings=underlying_embeddings,
    # Любое хранилище ByteStore для кеширования эмбеддингов документов.
    document_embedding_cache=store,
    # Пространство имён для кеша документов. Помогает избежать конфликтов (например, установите его на имя модели эмбеддинга).
    namespace=underlying_embeddings.model,
    query_embedding_cache=True,
)

# Пример: кеширование эмбеддинга текстового запроса
tic = time.time()
print(cached_embedder.embed_query("Привет, мир!"))
print(f"Первый вызов занял: {time.time() - tic:.2f} секунд")

# Последующие вызовы берут результат из кеша
tic = time.time()
print(cached_embedder.embed_query("Привет, мир!"))
print(f"Второй вызов занял: {time.time() - tic:.2f} секунд")
