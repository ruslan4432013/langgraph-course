from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def fake_nl_to_sql(query):
    # Заглушка преобразования NL → SQL
    return "SELECT id, text FROM docs LIMIT 2"


def fake_sql_execute(sql):
    # Заглушка выполнения SQL
    return [
        {"id": 1, "text": "Документ из реляционной базы."},
        {"id": 2, "text": "Еще один документ из SQL-базы."},
    ]


class SQLRetriever(BaseRetriever):
    def _get_relevant_documents(self, query):
        sql = fake_nl_to_sql(query)
        rows = fake_sql_execute(sql)
        docs = []
        for row in rows:
            docs.append(
                Document(
                    page_content=row["text"],
                    metadata={"id": row["id"], "sql": sql},
                )
            )
        return docs


if __name__ == "__main__":
    retriever = SQLRetriever()
    query = "найти документы про базы данных"
    result_docs = retriever.invoke(query)

    for doc in result_docs:
        print("Текст:", doc.page_content)
        print("Метаданные:", doc.metadata)
        print("-" * 40)
