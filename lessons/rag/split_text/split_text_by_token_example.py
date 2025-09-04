from pprint import pprint

from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(

    encoding_name="cl100k_base", chunk_size=100, chunk_overlap=0

)

with open("./sample_text.txt", "r") as f:
    document = f.read()

texts = text_splitter.split_text(document)

pprint(texts)
