# Введение в Document Loaders в LangChain

Этот раздел содержит примеры использования различных загрузчиков документов (Document Loaders) из библиотеки LangChain.
Загрузчики документов позволяют извлекать данные из различных источников и преобразовывать их в формат `Document`,
который затем может быть использован для индексации, поиска или обработки с помощью LLM.

## Содержание

1. [CSV Loader](#csv-loader)
2. [PDF Loader (PDFPlumber)](#pdf-loader-pdfplumber)
3. [Web Base Loader](#web-base-loader)

---

## Примеры

### 1. CSV Loader

Файл: `csv_loader_intro.py`

Пример демонстрирует загрузку данных из CSV-файла `data.csv`. В данном примере используется стандартный `CSVLoader`.

**Запуск:**

```bash
python src/loaders_intro/csv_loader_intro.py
```

### 2. PDF Loader (PDFPlumber)

Файл: `pdf_loader_intro.py`

Пример использования `PDFPlumberLoader` для чтения PDF-файлов. В данном случае используется асинхронный метод
`alazy_load()` для эффективного чтения страниц документа (на примере "Войны и мира").

**Запуск:**

```bash
python src/loaders_intro/pdf_loader_intro.py
```

### 3. Web Base Loader

Файл: `web_base_loader_intro.py`

Пример загрузки текстового контента с веб-страницы с использованием `WebBaseLoader`. Загрузчик извлекает текст из
HTML-кода страницы.

**Запуск:**

```bash
python src/loaders_intro/web_base_loader_intro.py
```

---

## Установка и настройка

### Предварительные требования

- Python 3.10+
- Установленные зависимости из `requirements.txt`

### Установка зависимостей

Из корневой директории проекта выполните:

```bash
pip install -r requirements.txt
```

### Настройка окружения

Для работы некоторых компонентов могут потребоваться ключи API (например, OpenAI), которые должны быть указаны в файле
`.env`. См. `src/settings.py` для ознакомления со структурой настроек.

## Структура файлов

- `data.csv` — пример данных для CSV загрузчика.
- `voina-i-mir.pdf` — пример документа для PDF загрузчика.
- `csv_loader_intro.py` — код примера для CSV.
- `pdf_loader_intro.py` — код примера для PDF.
- `web_base_loader_intro.py` — код примера для Web.
