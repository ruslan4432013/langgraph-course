# Примеры ретриверов в LangChain

Репозиторий с минимальными примерами реализации разных типов ретриверов на Python с использованием `langchain_core.retrievers.BaseRetriever` и `langchain_core.documents.Document`.

Каждый файл демонстрирует один паттерн: от простого in-memory ретривера до сложных ансамблей и мультивекторных схем. Примеры можно запускать как standalone-скрипты для проверки поведения и использовать как шаблоны для своих проектов.

***

## Общие требования

- Python ≥ 3.9
- Установка зависимостей:

```bash
pip install langchain-core
```

Все примеры используют только `langchain-core`, без привязки к конкретным векторным хранилищам или LLM-провайдерам.

***

## Список примеров

### `1_basic_retriever.py` — Простой in-memory ретривер

Базовый ретривер, хранящий документы в памяти и фильтрующий их по подстроке.

- Что делает:
  - Принимает список `Document` в конструкторе.
  - При запросе возвращает все документы, в которых текст содержит подстроку (без учёта регистра).
- Когда использовать:
  - Для быстрого прототипирования.
  - Когда нужен простой фильтр по ключевым словам, без векторов и сложных алгоритмов.

```python
retriever = SimpleInMemoryRetriever(docs)
result_docs = retriever.invoke("ретриверы")
```

***

### `2_vectorstore_as_retriever.py` — Ретривер на основе векторного хранилища

Показывает, как любое векторное хранилище (векторстор) можно превратить в ретривер через метод `as_retriever()`.

- Что делает:
  - Имитирует `VectorStore` с методом `similarity_search`.
  - Через `as_retriever()` получается `BaseRetriever`, который возвращает документы по семантической близости.
- Когда использовать:
  - Когда данные уже индексируются в векторсторе (Chroma, FAISS, Pinecone и т.п.).
  - Для RAG-сценариев, где важно искать по смыслу, а не по точному совпадению слов.

```python
vectorstore = DummyVectorStore(docs)
retriever = vectorstore.as_retriever()
result_docs = retriever.invoke("поиск")
```

***

### `3_search_api_retriever.py` — Ретривер поверх внешнего API

Ретривер, который не хранит документы, а вызывает внешний поисковый API (например, Amazon Kendra, Wikipedia Search и т.п.).

- Что делает:
  - Вызывает внешний API по запросу.
  - Преобразует «сырые» результаты (например, заголовки и URL) в список `Document`.
- Когда использовать:
  - Для интеграции с корпоративными поисковыми системами.
  - Когда документы живут в стороннем сервисе, а не в собственной базе.

```python
retriever = SearchApiRetriever()
result_docs = retriever.invoke("ретриверы langchain")
```

***

### `4_sql_retriever.py` — SQL-ретривер (NL → SQL)

Ретривер, преобразующий запрос на естественном языке в SQL, выполняющий его и возвращающий результаты как `Document`.

- Что делает:
  - Имитирует преобразование NL → SQL.
  - Выполняет SQL-запрос и оборачивает строки результата в `Document`.
- Когда использовать:
  - Когда данные хранятся в реляционной БД.
  - Для сценариев, где пользователь спрашивает о структурированных данных (например, «найти документы про базы данных»).

```python
retriever = SQLRetriever()
result_docs = retriever.invoke("найти документы про базы данных")
```

***

### `5_lexical_retriever.py` — Лексический ретривер (BM25 / TF-IDF)

Простой лексический ретривер, оценивающий релевантность по совпадению слов (аналог BM25 / TF-IDF).

- Что делает:
  - Подсчитывает количество совпавших слов между запросом и текстом документа.
  - Сортирует документы по «оценке» и возвращает только релевантные.
- Когда использовать:
  - Для поиска по точным терминам и ключевым словам.
  - В комбинации с векторным поиском (ансамбль) для улучшения точности.

```python
retriever = SimpleLexicalRetriever(docs)
result_docs = retriever.invoke("лексический поиск BM25")
```

***

### `6_ensemble_retriever.py` — Ансамблевый ретривер

Ретривер, объединяющий несколько других ретриверов (например, векторный + лексический) с помощью алгоритма вроде Reciprocal Rank Fusion.

- Что делает:
  - Принимает список ретриверов и их весов.
  - Запускает каждый ретривер, объединяет результаты и пересортирует по общей оценке.
- Когда использовать:
  - Когда один тип поиска (только векторный или только лексический) даёт низкую точность.
  - Для гибридного поиска, где важно учитывать и смысл, и точные термины.

```python
ensemble_retriever = SimpleEnsembleRetriever(
    retrievers=[retriever_a, retriever_b],
    weights=[0.5, 0.5]
)
result_docs = ensemble_retriever.invoke("любой запрос")
```

***

### `7_parent_document_retriever.py` — Parent Document Retriever

Ретривер, который ищет по фрагментам (чанкам), но возвращает целые «родительские» документы, сохраняя контекст.

- Что делает:
  - Хранит связь «родительский документ → дочерние фрагменты».
  - По запросу находит релевантные фрагменты, а возвращает соответствующие родительские документы.
- Когда использовать:
  - Когда документы сильно режутся на чанки для индексации.
  - Чтобы избежать потери общего контекста и возвращать пользователю полный документ.

```python
retriever = ParentDocumentRetriever(store, child_vectorstore)
result_docs = retriever.invoke("детали ретриверов")
```

***

### `8_multi_vector_retriever.py` — Multi Vector Retriever

Ретривер, создающий несколько векторов для одного документа (например, краткое содержание, гипотетические вопросы) и возвращающий исходный документ.

- Что делает:
  - Для одного `Document` создаёт несколько представлений (summary, questions и т.п.).
  - Индексирует векторы по этим представлениям, но при поиске возвращает исходный документ.
- Когда использовать:
  - Когда есть возможность генерировать альтернативные представления документа (например, через LLM).
  - Для улучшения recall: документ может быть найден по разным формулировкам запроса.

```python
retriever = MultiVectorRetriever(index)
result_docs = retriever.invoke("несколько векторов на один документ")
```

***

## Как использовать

1. Установите зависимости:

```bash
pip install langchain-core
```

2. Запустите любой пример:

```bash
python 1_basic_retriever.py
python 2_vectorstore_as_retriever.py
# и так далее
```

3. Для интеграции в своё приложение:
   - Скопируйте нужный класс ретривера.
   - Замените заглушки (`DummyVectorStore`, `fake_search_api`, `fake_nl_to_sql` и т.п.) на реальные интеграции.
   - Используйте ретривер как `Runnable` в LCEL-цепочках или напрямую через `invoke(query)`.

***

## Лицензия

MIT. Можно свободно использовать, модифицировать и распространять код.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/07857261-b139-467c-8485-1c2cc5f51bef/2_vectorstore_as_retriever.py)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/9c211116-c994-4d70-abf6-730a7b74008f/5_lexical_retriever.py)
[3](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/fb720393-552f-4700-9bd7-06bc829e56ff/7_parent_document_retriever.py)
[4](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/34760477-276f-443d-9954-b63570298320/6_ensemble_retriever.py)
[5](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/feb507f5-4525-4718-97a1-a46d274a7e08/3_search_api_retriever.py)
[6](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/e8151063-1b6f-4ab7-b621-7d66c5a5beac/4_sql_retriever.py)
[7](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/a30bfd39-d1ba-472a-99ca-f023171670b9/8_multi_vector_retriever.py)
[8](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/d4e2a3ba-fde7-4d51-b500-2f54be183c8c/1_basic_retriever.py)
[9](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/c4b6babc-b1fa-47b2-b465-0ba7dd385954/3_search_api_retriever.py)
[10](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/150851267/abfc4b93-1ce1-4a33-a8f9-f87a1b63cbbb/7_parent_document_retriever.py)