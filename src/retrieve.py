from langchain_core.documents import Document

facts = [
    "Зир’фан из туманности Орфелия",
    "Полупрозрачное тело с биолюминесцентными жилами, меняющими цвет по эмоциям",
    "Общается через резонансные колебания костей черепа собеседника, без звуков",
    "Питается звездным ветром, фильтруя заряженные частицы через хитиновый гребень на спине",
    "Время воспринимает нелинейно и помнит будущие «эхо-варианты», избегая опасностей заранее"
]


def retrieve(query: str) -> list[Document]:
    # Здесь мы имитируем запрос в векторное хранилище и получаем список Document
    docs = [Document(page_content=fact, metadata={"animal": "Zir'fan"}) for fact in facts]
    return docs


query_docs = retrieve("Зир'фан")

context = '\n'.join([doc.page_content for doc in query_docs])
