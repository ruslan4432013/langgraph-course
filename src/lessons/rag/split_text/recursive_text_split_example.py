import pprint

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

with open("./sample_text.txt", "r") as f:
    document = f.read()

texts = text_splitter.split_text(document)
pprint.pprint(texts)

documents = text_splitter.create_documents([document])
pprint.pprint(documents)
