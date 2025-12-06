"""
Пример 7: Структура Document объектов
Демонстрирует: компоненты Document с page_content и metadata
"""

from langchain_core.documents import Document

print("=" * 60)
print("СТРУКТУРА DOCUMENT ОБЪЕКТОВ")
print("=" * 60)

# Создание различных документов с метаданными
documents = [
    Document(
        page_content="Искусственный интеллект революционизирует технологию.",
        metadata={
            "source": "research_paper",
            "author": "John Doe",
            "year": 2024,
            "tags": ["AI", "technology"],
        },
    ),
    Document(
        page_content="Рецепт пасты: варить макароны 10 минут.",
        metadata={
            "source": "recipe_blog",
            "author": "Chef Maria",
            "cuisine": "Italian",
            "prep_time": 15,
        },
    ),
    Document(
        page_content="Последние новости о климатических изменениях.",
        metadata={
            "source": "news_article",
            "date": "2024-12-02",
            "category": "science",
        },
    ),
]

# Вывод информации о каждом документе
for i, doc in enumerate(documents, 1):
    print(f"\n{'─' * 60}")
    print(f"ДОКУМЕНТ {i}")
    print(f"{'─' * 60}")
    print(f"\n📄 Содержание (page_content):")
    print(f"  {doc.page_content}")
    print(f"\n🏷️  Метаданные (metadata):")
    for key, value in doc.metadata.items():
        print(f"  • {key}: {value}")

print(f"\n{'=' * 60}")
print("КЛЮЧЕВЫЕ КОМПОНЕНТЫ:")
print("=" * 60)
print("\n✓ page_content: Основной текст документа")
print("✓ metadata: Словарь с дополнительной информацией")
print("  - source: Источник документа (tweet, news, article и т.д.)")
print("  - date/time: Временные метки")
print("  - author: Автор документа")
print("  - tags/categories: Классификация")
print("  - Любые другие релевантные поля")
print("\n💡 Метаданные помогают фильтровать результаты поиска!")
