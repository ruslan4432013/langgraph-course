# Подход 1 — Разделение по длине (по токенам)
from langchain_text_splitters import CharacterTextSplitter

with open("./rag_article.txt", "r") as f:
    document = f.read()

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-4", chunk_size=10, chunk_overlap=0
)

texts = text_splitter.split_text(document)

for i, text in enumerate(texts, start=1):
    print('-' * 50)
    print(f"Chunk: {i}")
    print(text)
    print(len(text))

# text_splitter_1 = TokenTextSplitter(chunk_size=10, chunk_overlap=0)
#
# texts = text_splitter_1.split_text(document)
#
# for i, text in enumerate(texts, start=1):
#     print('-' * 50)
#     print(f"Chunk: {i}")
#     print(text)
#     print(len(text))
