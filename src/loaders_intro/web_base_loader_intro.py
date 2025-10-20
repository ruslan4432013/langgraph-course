import asyncio

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://habr.com/ru/articles/307252/", verify_ssl=False)


async def load_documents():
    documents = loader.load()
    for i, document in enumerate(documents):
        print('-' * 50)
        print(f"DOCUMENT {i}:")
        print(document.page_content.replace("\n", " ").strip())
        print('-' * 50)


if __name__ == '__main__':
    asyncio.run(load_documents())
