# 🚀 LangChain Vector Stores — Практические примеры

[![LangChain](https://img.shields.io/badge/LangChain-VectorStores-blueviolet?style=for-the-badge&logo=langchain)](https://python.langchain.com/docs/integrations/vectorstores/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen?style=for-the-badge&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**10 готовых примеров** для освоения векторных хранилищ LangChain. От базового CRUD до продвинутых RAG-концепций.

## 📋 Содержимое репозитория

| # | Файл | Что демонстрирует | Время запуска |
|---|------|-------------------|---------------|
| `1_initialization.py` | Инициализация `InMemoryVectorStore` + OpenAI | **30 сек** |
| `2_adding_documents.py` | `Document` + `add_documents(ids=...)` | **45 сек** |
| `3_similarity_search.py` | Семантический поиск `similarity_search()` | **1 мин** |
| `4_deletion.py` | Удаление `delete(ids=...)` | **45 сек** |
| `5_metadata_filtering.py` | Метаданные + фильтрация (концепция) | **1 мин** |
| `6_similarity_metrics.py` | Косинус, L2, Dot Product | **1.5 мин** |
| `7_document_structure.py` | Структура `Document(page_content, metadata)` | **45 сек** |
| `8_search_parameters.py` | Параметры `k`, `filter`, `query` | **1 мин** |
| **`9_complete_workflow.py`** | 🔥 **Полный RAG цикл** (копипаст в проект) | **2 мин** |
| `10_advanced_concepts.py` | MMR, HNSW, масштабирование | **2 мин** |

## 🎯 Быстрый старт (3 минуты)

```
# 1. Клонировать
git clone <repo-url>
cd langchain-vector-stores

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить OpenAI
cp .env.example .env
# редактируем .env: OPENAI_API_KEY=sk-...

# 4. Запустить основной пример!
python 9_complete_workflow.py
```

## 📦 Установка зависимостей

```
# requirements.txt
langchain-core>=0.2.0
langchain-openai>=0.1.0
python-dotenv>=1.0.0
```

## ⚙️ Конфигурация `.env`

```
# .env.example → .env
OPENAI_API_KEY=sk-proj-...
OPENAI_BASE_URL=https://api.openai.com/v1

# Локальная LLM (Ollama):
# OPENAI_BASE_URL=http://localhost:11434/v1
```

## 🚀 Пошаговое обучение

```
┌─ 1→2→3→4 ─── БАЗОВЫЙ CRUD ───────┐  [5 мин]
│                                    │
├─ 5→7 ────── МЕТАДАННЫЕ ───────────┤  [2 мин] 
│                                    │
├─ 6→8 ────── МЕТРИКИ+ПАРАМЕТРЫ ────┤  [3 мин]
│                                    │
├─ 9 ──────── FULL WORKFLOW 🔥 ─────┤  [2 мин]
│                                    │
└─ 10 ─────── ADVANCED ──────────────┘  [2 мин]
```

**⭐ MVP для RAG**: `9_complete_workflow.py` — копируйте в продакшен!

## 📱 Пример вывода

```
$ python 3_similarity_search.py
✓ Поиск по сходству выполнен
Запрос: 'искусственный интеллект и нейронные сети'
Найдено результатов (k=2):

1. Машинное обучение — это область искусственного интеллекта.
   Источник: AI_guide

2. Нейронные сети используются для обработки сложных данных.
   Источник: AI_guide
```

## 🎓 Уровни сложности

| Уровень | Примеры | Для кого |
|---------|---------|----------|
| **Новичок** | 1-4, 7, 9 | Базовый API |
| **Middle** | 5, 6, 8 | Метрики + параметры |
| **Senior** | 10 | Масштабирование + MMR |

## 🔍 Сравнение векторных хранилищ

| Сценарий | Хранилище | Размер | Фильтры | Персистентность | Пример |
|----------|-----------|--------|---------|-----------------|--------|
| **Прототип** | `InMemoryVectorStore` | <10K | ❌ | Память | ✅ **этот репозиторий** |
| **Малый prod** | Chroma, FAISS | 10K-1M | ✅ | Файл | `10_advanced_concepts.py` |
| **Большой prod** | Pinecone, Qdrant | 1M+ | ✅✅ | Облако | `10_advanced_concepts.py` |

## 💡 Ключевые концепции

```
Document = page_content (текст) + metadata (source, date, tags) + ID
↓
add_documents(ids=["doc1"]) → эмбеддинги → индекс
↓
similarity_search("запрос", k=4, filter={"source": "article"})
↓
delete(ids=["doc1"]) → обновление данных
```

## 🎬 Дополнительные ресурсы

- [📖 LangChain VectorStores](https://python.langchain.com/docs/integrations/vectorstores/)
- [📱 Видео-урок](https://youtube.com/...) — 8 минут практика
- [📄 Методичка](3_6_Vector_storage.html) — официальная документация

## 🛠️ Разработка

```
# Форматирование
black .
isort .

# Линтинг
flake8 .
mypy .

# Тестирование
pytest tests/
```

## 🤝 Вклад

1. Форк → изменения → PR
2. Новые примеры: `11_*.py` по нумерации
3. `black . && isort .` перед пушем

## 📄 Лицензия

[MIT](LICENSE) — свободное использование в коммерции, курсах, продакшене.

---

<div align="center">

**⭐ Если помогло — дайте звезду!**  
**🚀 Готово к продакшену за 5 минут**  
**📅 Декабрь 2025**

</div>
