from src.applications.web_rag_app.app_parts.document_splitting import all_splits
from src.components.vector_store_client import vector_store

document_ids = vector_store.add_documents(documents=all_splits)

print(document_ids[:3])
