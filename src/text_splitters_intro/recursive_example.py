from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

with open("./rag_article.txt", "r") as f:
    document = f.read()

texts = text_splitter.split_text(document)
print(f"Number of chunks: {len(texts)}")

for i, text in enumerate(texts, start=1):
    print('-' * 50)
    print(f"Chunk: {i}")
    print(text)
    print(len(text))
