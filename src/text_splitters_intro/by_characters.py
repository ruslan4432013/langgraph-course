# Подход 1 — Разделение по длине (по символам/словам)
from langchain_text_splitters import CharacterTextSplitter

with open("./rag_article.txt", "r") as f:
    document = f.read()

text_splitter = CharacterTextSplitter(
    separator=' ',
    chunk_size=15,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

text_documents = text_splitter.create_documents([document])
split_text = text_splitter.split_text(document)

for i, text in enumerate(split_text, start=1):
    print('-' * 50)
    print(f"Chunk: {i}")
    print(text)
    print(len(text))
