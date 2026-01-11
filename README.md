# Введение в Text Splitters в LangChain

Этот проект содержит примеры использования различных инструментов для разделения текста (Text Splitters) из библиотеки
LangChain. Разделение текста на фрагменты (chunks) является важным этапом при создании RAG (Retrieval-Augmented
Generation) систем.

## Содержание

В директории `src/text_splitters_intro/` представлены следующие примеры:

1. **Разделение по символам (`by_characters.py`)**  
   Использование `CharacterTextSplitter` для простого разделения текста по заданному разделителю (например, пробелу) с
   фиксированным размером фрагмента.

2. **Разделение по токенам (`by_token_length.py`)**  
   Использование `CharacterTextSplitter.from_tiktoken_encoder` для разделения текста на основе количества токенов (
   используется кодировщик `gpt-4`). Это полезно для точного контроля лимитов контекстного окна LLM.

3. **Рекурсивное разделение (`recursive_example.py`)**  
   Использование `RecursiveCharacterTextSplitter`. Этот сплиттер пытается сохранить смысловую целостность (например,
   абзацы или предложения), пробуя разные разделители по очереди. Это рекомендуемый способ для большинства текстовых
   задач.

4. **Разделение кода (`code_splitter.py`)**  
   Пример использования `RecursiveCharacterTextSplitter.from_language` для разделения исходного кода Python. Сплиттер
   учитывает синтаксис языка (классы, функции, отступы).

5. **Семантическое разделение (`semantic_splitter.py`)**  
   Использование `SemanticChunker`. Метод разделяет текст на основе семантической схожести предложений, используя
   эмбеддинги. Позволяет группировать логически связанные части текста.

## Установка

1. Клонируйте репозиторий.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

Для работы семантического сплиттера и других компонентов необходимо настроить переменные окружения. Создайте файл `.env`
в корне проекта:

```env
OPENAI_API_KEY=your_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=your_project_name
```

*Примечание: В `semantic_splitter.py` используется прокси-база для OpenAI (`https://api.proxyapi.ru/openai/v1`).*

## Запуск примеров

Скрипты следует запускать как модули из корня проекта:

```bash
python -m src.text_splitters_intro.by_characters
python -m src.text_splitters_intro.by_token_length
python -m src.text_splitters_intro.recursive_example
python -m src.text_splitters_intro.code_splitter
python -m src.text_splitters_intro.semantic_splitter
```

## Материалы

- `src/text_splitters_intro/rag_article.txt` — пример текстового файла, используемый в скриптах.
