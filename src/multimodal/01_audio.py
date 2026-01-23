import base64
from pathlib import Path

from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.settings import settings

# Использование модели gpt-4o-audio-preview для аудио
model = ChatOpenAI(
    model="gpt-4o-audio-preview",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# 1. Основы работы с аудио-сообщениями
# Контент сообщения может содержать аудио-блоки

current_file = Path(__file__).resolve()
# Путь к аудио-файлу (убедитесь, что файл существует)
audio_path = current_file.parent.parent / "resources" / "animal.wav"

if audio_path.exists():
    with open(audio_path, "rb") as f:
        audio_data = base64.standard_b64encode(f.read()).decode("utf-8")

    audio_block = {"type": "audio", "base64": audio_data, "mime_type": "audio/wav"}

    # Пример сообщения с текстом и аудио
    message = HumanMessage(content=[
        {"type": "text", "text": "Что говорят в этом аудио?"},
        audio_block,
    ])

    if __name__ == "__main__":
        print("Отправка запроса с аудио...")
        result = model.invoke([message])
        print(f"Ответ модели: {result.content}")
else:
    print(f"Файл {audio_path} не найден. Пожалуйста, добавьте аудио-файл в папку resources.")
