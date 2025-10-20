from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path="./data.csv",
)
data = loader.load()

for doc in data:
    print(doc)
