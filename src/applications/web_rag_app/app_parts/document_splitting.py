from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.applications.web_rag_app.app_parts.web_loader import docs

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # размер фрагмента (символов)
    chunk_overlap=200,  # перекрытие фрагментов (символов)
    add_start_index=True,  # отслеживать индекс в исходном документе
)
all_splits = text_splitter.split_documents(docs)

total_documents = len(all_splits)
third = total_documents // 3

for i, document in enumerate(all_splits):
    if i < third:
        document.metadata["section"] = "beginning"
    elif i < 2 * third:
        document.metadata["section"] = "middle"
    else:
        document.metadata["section"] = "end"
