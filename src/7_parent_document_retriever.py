from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class ParentDocumentStore:
    def __init__(self):
        self.parents = {}
        self.children = {}

    def add_parent(self, parent_id, document):
        self.parents[parent_id] = document

    def add_child(self, child_id, parent_id, document):
        self.children[child_id] = {"parent_id": parent_id, "doc": document}

    def get_parent_by_child(self, child_id):
        parent_id = self.children[child_id]["parent_id"]
        return self.parents[parent_id]


class DummyChildVectorStore:
    def __init__(self, child_ids):
        self.child_ids = child_ids

    def similarity_search_child_ids(self, query, k=2):
        # Заглушка: просто вернуть первые k child_id
        return self.child_ids[:k]


class ParentDocumentRetriever(BaseRetriever):
    def __init__(self, store, child_vectorstore):
        super().__init__()
        self._store = store
        self._child_vectorstore = child_vectorstore

    def _get_relevant_documents(self, query):
        child_ids = self._child_vectorstore.similarity_search_child_ids(query, k=2)
        parents = []
        seen = set()
        for child_id in child_ids:
            parent_doc = self._store.get_parent_by_child(child_id)
            if id(parent_doc) not in seen:
                parents.append(parent_doc)
                seen.add(id(parent_doc))
        return parents


if __name__ == "__main__":
    store = ParentDocumentStore()

    parent_doc = Document(
        page_content="Большой документ о ретриверах, разбитый на фрагменты.",
        metadata={"id": "parent1"},
    )
    store.add_parent("parent1", parent_doc)

    child1 = Document(page_content="Фрагмент 1: вводная часть.", metadata={"child_id": "c1"})
    child2 = Document(page_content="Фрагмент 2: детали реализации.", metadata={"child_id": "c2"})

    store.add_child("c1", "parent1", child1)
    store.add_child("c2", "parent1", child2)

    child_vectorstore = DummyChildVectorStore(child_ids=["c1", "c2"])

    retriever = ParentDocumentRetriever(store, child_vectorstore)

    query = "детали ретриверов"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("РОДИТЕЛЬСКИЙ ДОКУМЕНТ:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
