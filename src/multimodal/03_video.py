# Multimedia video example
import base64
import pprint
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.settings import settings

# Примечание: Поддержка видео зависит от провайдера (например, Gemini 1.5)
model = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    base_url='https://api.proxyapi.ru/google',
    api_key=settings.OPENAI_API_KEY
)

# 2. Видео по File ID
message_video_file_id = HumanMessage(content=[
    {"type": "text", "text": "Что происходит в этом видео?"},
    {"type": "media", "file_id": "file-abc123"},
])

if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    video_path = current_file.parent.parent / "resources" / "animal.mp4"
    with open(video_path, "rb") as f:
        video_data = base64.standard_b64encode(f.read()).decode("utf-8")

    recognize_message = HumanMessage(content=[
        {"type": "text", "text": "Опишите содержимое этого видео."},
        {
            "type": "video",
            "base64": video_data,
            "mime_type": "video/mp4",
        },
    ])

    result = model.invoke([recognize_message])

    pprint.pprint(result.content)
