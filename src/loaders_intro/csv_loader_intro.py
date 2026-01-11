import os

from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = os.path.join(os.path.dirname(__file__), "data.csv")

loader = CSVLoader(
    file_path=file_path,
    csv_args={
        'delimiter': ';',
    }
)
data = loader.load()

for doc in data:
    print(doc)
