import asyncio
import os

from langchain_community.document_loaders import PDFPlumberLoader

file_path = os.path.join(os.path.dirname(__file__), "voina-i-mir.pdf")

loader = PDFPlumberLoader(file_path, extract_images=False)


async def load_documents():
    i = 1
    all_documents = []
    async for document in loader.alazy_load():
        print('-' * 50)
        print(f"DOCUMENT {i}:")
        print(document)
        all_documents.append(document)
        print('-' * 50)
        i += 1

    print(len(all_documents))

    return all_documents


if __name__ == '__main__':
    asyncio.run(load_documents())
