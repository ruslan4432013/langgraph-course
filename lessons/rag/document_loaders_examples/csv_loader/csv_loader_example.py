import pprint

from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path="data.csv",
)
data = loader.load()

loader.alazy_load()

if __name__ == "__main__":
    pprint.pprint(data)
