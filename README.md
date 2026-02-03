# Agentic RAG + ChainRAG: Учебный пример

Данный проект представляет собой учебный пример реализации систем **RAG (Retrieval-Augmented Generation)** с
использованием библиотеки **LangGraph**. В проекте продемонстрированы два подхода к архитектуре: классическая
последовательная цепочка (**ChainRAG**) и гибкий агент (**Agentic RAG**).

## Основные концепции

### 1. ChainRAG (Последовательный RAG)

Реализован в `src/web_rag_application/web_rag_application.py`.
Этот подход следует структурированному графу состояний:

* **query_or_respond**: Узел принимает решение — вызвать инструмент поиска или ответить пользователю сразу.
* **tools**: Выполнение поиска (retrieval) в векторном хранилище FAISS.
* **generate**: Генерация финального ответа на основе контекста из найденных документов.

### 2. Agentic RAG

Реализован в `src/web_rag_application/web_rag_application_agent.py`.
Использует высокоуровневый интерфейс создания агентов, который позволяет системе:

* Самостоятельно определять необходимость вызова инструментов.
* Выполнять сложные многошаговые рассуждения.
* Сохранять состояние диалога благодаря `MemorySaver`.

## Структура проекта

* `src/web_rag_application/` — Логика RAG-приложения.
    * `web_rag_application.py` — Конфигурация графа ChainRAG.
    * `web_rag_application_agent.py` — Конфигурация Agentic RAG.
    * `nodes.py` — Реализация функций-узлов графа.
    * `tools/retrieve.py` — Инструмент для поиска информации.
* `src/components/` — Инфраструктурные модули.
    * `llm_model.py` — Настройка языковой модели (ChatOpenAI).
    * `embedding.py` — Настройка модели эмбеддингов.
    * `vector_store_client.py` — Инициализация векторной базы данных FAISS.
* `main.py` — Пример запуска системы с тестовым запросом.
* `langgraph.json` — Манифест для LangGraph, определяющий точки входа в графы.

## Настройка и запуск

### Предварительные требования

* Python 3.10+
* Ключ OpenAI API

### Установка

1. Установите необходимые пакеты:
   ```bash
   pip install -r requirements.txt
   ```
2. Создайте файл `.env` в корне проекта и заполните его:
   ```env
   OPENAI_API_KEY=your_api_key
   LANGSMITH_API_KEY=your_key (опционально)
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_PROJECT="your_project_name"
   ```

### Запуск

Для демонстрации работы агента выполните:

```bash
python main.py
```

Проект автоматически загружает содержимое
статьи [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) в качестве базы знаний для
RAG.

## Технологический стек

* **LangGraph** — оркестрация графов состояний.
* **LangChain** — работа с LLM и инструментами.
* **FAISS** — векторное хранилище.
* **BeautifulSoup** — парсинг веб-контента.
