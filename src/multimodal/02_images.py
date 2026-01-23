import base64
from pprint import pprint

from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.settings import settings

# Использование модели gpt-5.2 для изображений
model = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# 1. Изображение по URL
message_url = HumanMessage(content=[
    {"type": "text", "text": "Опишите содержимое этого изображения."},
    {"type": "image", "url": "https://drive.usercontent.google.com/download?id=1AVDOvvl-dpdfJc_v8vOb1v3lnBkxJSAn"},
])

if __name__ == "__main__":
    response = model.invoke(input=[message_url])
    pprint(response.content)
    pass


# 2. Изображение из base64
# ВАЖНО: При использовании base64 обязательно указывайте mime_type
def get_image_message_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return HumanMessage(
        content=[
            {"type": "text", "text": "Что изображено на этой картинке?"},
            {
                "type": "image",
                "base64": image_data,
                "mime_type": "image/jpeg",
            },
        ]
    )


# 3. Изображение по File ID (для предварительно загруженных файлов у провайдера)
message_file_id = HumanMessage(
    content=[
        {"type": "text", "text": "Опишите это изображение."},
        {"type": "image", "file_id": "file-abc123"},
    ]
)

# 4. Использование класса HumanMessage
human_msg = HumanMessage(content=[
    {"type": "text", "text": "Что вы видите на изображении?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])
