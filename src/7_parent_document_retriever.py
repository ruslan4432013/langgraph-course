from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class ParentDocumentStore:
    """Хранилище для родительских и дочерних документов."""

    def __init__(self):
        # Хранит полные (родительские) документы по их ID
        self.parents = {}
        # Хранит метаданные дочерних фрагментов и их связь с родителями
        self.children = {}

    def add_parent(self, parent_id, document):
        """Добавить основной документ в хранилище."""
        self.parents[parent_id] = document

    def add_child(self, child_id, parent_id, document):
        """Добавить фрагмент документа и связать его с родителем."""
        self.children[child_id] = {"parent_id": parent_id, "doc": document}

    def get_parent_by_child(self, child_id):
        """Найти родительский документ по ID его фрагмента."""
        parent_id = self.children[child_id]["parent_id"]
        return self.parents[parent_id]


class DummyChildVectorStore:
    """Заглушка векторного хранилища для поиска по фрагментам."""

    def __init__(self, child_ids):
        self.child_ids = child_ids

    def similarity_search_child_ids(self, query, k=2):
        """Имитация поиска: просто возвращает первые k ID фрагментов."""
        # Заглушка: просто вернуть первые k child_id
        return self.child_ids[:k]


class ParentDocumentRetriever(BaseRetriever):
    """Ретривер, который ищет по фрагментам, но возвращает целые документы."""

    def __init__(self, store, child_vectorstore):
        super().__init__()
        self._store = store
        self._child_vectorstore = child_vectorstore

    def _get_relevant_documents(self, query):
        # 1. Ищем релевантные ФРАГМЕНТЫ (дочерние документы) через векторный поиск
        child_ids = self._child_vectorstore.similarity_search_child_ids(query, k=2)
        parents = []
        seen = set()
        for child_id in child_ids:
            # 2. Для каждого найденного фрагмента находим его РОДИТЕЛЯ в основном хранилище
            parent_doc = self._store.get_parent_by_child(child_id)

            # 3. Добавляем родителя в результат, если он еще не был добавлен (избегаем дублей)
            if id(parent_doc) not in seen:
                parents.append(parent_doc)
                seen.add(id(parent_doc))
        return parents


if __name__ == "__main__":
    # Инициализация хранилища связей
    store = ParentDocumentStore()

    # Создание родительского документа
    parent_doc = Document(
        page_content="Большой документ о ретриверах, разбитый на фрагменты.",
        metadata={"id": "parent1"},
    )
    store.add_parent("parent1", parent_doc)

    # Создание дочерних фрагментов (частей документа)
    child1 = Document(page_content="Фрагмент 1: вводная часть.", metadata={"child_id": "c1"})
    child2 = Document(page_content="Фрагмент 2: детали реализации.", metadata={"child_id": "c2"})

    # Сохранение связей между фрагментами и их родителем
    store.add_child("c1", "parent1", child1)
    store.add_child("c2", "parent1", child2)

    # Создание векторного хранилища с ID фрагментов
    child_vectorstore = DummyChildVectorStore(child_ids=["c1", "c2"])

    # Создание итогового ретривера
    retriever = ParentDocumentRetriever(store, child_vectorstore)

    # Пример запроса
    query = "детали ретриверов"
    # Запуск процесса поиска
    result_docs = retriever.invoke(query)

    # Вывод результатов
    for doc in result_docs:
        print("РОДИТЕЛЬСКИЙ ДОКУМЕНТ:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
