"""
Настройка окружения для RAG-агента с LangGraph.

Документация:
- LangGraph: https://langchain-ai.github.io/langgraph/
- LangChain OpenAI: https://python.langchain.com/docs/integrations/platforms/openai/
- Установка пакетов: https://python.langchain.com/docs/get_started/installation/
"""

import getpass
import os


def _set_env(key: str):
    """Установка переменной окружения с запросом ввода, если она не задана."""
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")


# Установка API-ключа OpenAI
_set_env("OPENAI_API_KEY")

# Опционально: для трассировки в LangSmith
# _set_env("LANGSMITH_API_KEY")
# os.environ["LANGSMITH_TRACING"] = "true"

print("✅ Окружение настроено успешно!")
print(f"   OPENAI_API_KEY установлен: {'OPENAI_API_KEY' in os.environ}")