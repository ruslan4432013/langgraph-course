# Учебный пример RAG на LangChain

Данный проект является введением в концепцию **RAG (Retrieval-Augmented Generation)** с использованием библиотеки
LangChain.

## Описание

Проект демонстрирует базовый цикл работы RAG:

1. **Retrieval (Извлечение)**: Поиск релевантной информации по запросу пользователя. В данном примере поиск имитируется
   в файле `src/retrieve.py` с использованием предопределенного списка фактов о вымышленном существе Зир'фан.
2. **Augmentation (Обогащение)**: Добавление найденного контекста в промпт для языковой модели.
3. **Generation (Генерация)**: Получение ответа от LLM на основе предоставленного контекста.

## Структура проекта

* `src/main.py` — основной файл запуска. Здесь настраивается цепочка (Chain), объединяющая промпт, контекст и LLM.
* `src/retrieve.py` — логика "извлечения" данных. Содержит базу знаний и функцию для формирования контекста.
* `src/settings.py` — конфигурация приложения (API ключи, настройки модели) с использованием Pydantic Settings.
* `src/document_example.py` — пример работы с объектом `Document` в LangChain.
* `requirements.txt` — список необходимых зависимостей.

## Установка

1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   # или
   venv\Scripts\activate     # Для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

Создайте файл `.env` в корневом каталоге и добавьте следующие переменные:

```env
OPENAI_API_KEY=your_openai_api_key

# Настройки для LangSmith (опционально)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_project_name
```

*Примечание: В `src/main.py` используется `base_url="https://api.proxyapi.ru/openai/v1"`, что позволяет использовать
прокси для доступа к OpenAI API.*

## Запуск

Для запуска основного примера выполните команду:

```bash
python -m src.main
```

Программа задаст вопрос: *"Как общается Зир'фан?"* и сгенерирует ответ, основываясь на фактах из `src/retrieve.py`.

## Как это работает (код)

В `src/main.py` создается шаблон промпта:

```python
prompt_template = ChatPromptTemplate([
    ("system", "Ты — полезный помощник. Используй следующий контекст, чтобы ответить на вопрос..."),
    ("user", "{question}")
])
```

Затем создается цепочка с помощью LCEL (LangChain Expression Language):

```python
chain = prompt_template | llm
```

При вызове `chain.invoke` мы передаем и вопрос, и извлеченный контекст:

```python
response = chain.invoke({
    "question": question,
    "context": context,
})
```
