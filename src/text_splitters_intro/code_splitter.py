from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=100, chunk_overlap=0
)

with open("./recursive_example.py", "r") as f:
    PYTHON_CODE = f.read()

python_docs = python_splitter.create_documents([PYTHON_CODE])

for i, doc in enumerate(python_docs, start=1):
    print('-' * 50)
    print(f"Chunk: {i}")
    print(doc.page_content)
