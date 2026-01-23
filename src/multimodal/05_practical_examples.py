import base64
from pathlib import Path
from pprint import pprint

from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.settings import settings

# Настройка моделей
# Для большинства мультимодальных задач (изображения, PDF) используем gpt-4o
model = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# Для аудио используем специализированную модель gpt-4o-audio-preview
audio_model = ChatOpenAI(
    model="gpt-4o-audio-preview",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# Определение путей к ресурсам
# current_file указывает на src/multimodal/05_practical_examples.py
# resources_dir будет указывать на src/resources
current_file = Path(__file__).resolve()
resources_dir = current_file.parent.parent / "resources"


# Пример 1: Анализ изображения по URL
def analyze_image_example():
    print("\n--- Пример 1: Анализ изображения ---")
    message = HumanMessage(content=[
        {"type": "text", "text": "Что изображено на этой фотографии?"},
        {
            "type": "image",
            "url": "https://drive.usercontent.google.com/download?id=1AVDOvvl-dpdfJc_v8vOb1v3lnBkxJSAn"
        },
    ])

    response = model.invoke([message])
    pprint(response.content)


# Пример 2: Транскрипция и анализ аудио
def transcribe_audio_example():
    print("\n--- Пример 2: Транскрипция аудио ---")
    audio_path = resources_dir / "animal.wav"

    if not audio_path.exists():
        print(f"Файл {audio_path} не найден. Пропуск примера.")
        return

    with open(audio_path, "rb") as f:
        audio_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = HumanMessage(content=[
        {"type": "text", "text": "Пожалуйста, транскрибируйте эту аудиозапись и опишите звуки."},
        {
            "type": "audio",
            "base64": audio_data,
            "mime_type": "audio/wav",
        },
    ])

    response = audio_model.invoke([message])
    pprint(response.content)


# Пример 3: Анализ PDF-документа (через блоки контента)
def analyze_pdf_example():
    print("\n--- Пример 3: Анализ PDF-документа ---")
    pdf_path = resources_dir / "rental.pdf"

    if not pdf_path.exists():
        print(f"Файл {pdf_path} не найден. Пропуск примера.")
        return

    with open(pdf_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    messages = [
        SystemMessage(content="Вы эксперт по анализу юридических документов."),
        HumanMessage(content=[
            {"type": "text", "text": "Извлеките основные условия аренды и сумму депозита из этого договора."},
            {
                "type": "file",
                "base64": pdf_data,
                "mime_type": "application/pdf",
                "filename": "rental.pdf",
            },
        ])
    ]

    response = model.invoke(messages)
    pprint(response.content)


# Пример 4: Комбинированный мультимодальный запрос (Текст + Изображение)
def combined_multimodal_example():
    print("\n--- Пример 4: Комбинированный запрос (Текст + Изображение) ---")
    image_url = "https://drive.usercontent.google.com/download?id=1AVDOvvl-dpdfJc_v8vOb1v3lnBkxJSAn"

    message = HumanMessage(content=[
        {"type": "text", "text": "Проанализируйте это изображение:"},
        {"type": "image", "url": image_url},
        {"type": "text", "text": "Какие эмоции может вызывать эта фотография у зрителя?"},
    ])

    response = model.invoke([message])
    pprint(response.content)


# Пример 5: Использование нескольких блоков (Сравнение изображений)
def compare_images_example():
    print("\n--- Пример 5: Сравнение изображений ---")
    message = HumanMessage(content=[
        {"type": "text", "text": "Сравни эти два изображения. Чем они отличаются?"},
        {
            "type": "image",
            "url": "https://drive.usercontent.google.com/download?id=1MJIb73X5WDEXosnhtUd93lkUbEhC4McY"
        },
        {
            "type": "image",
            "url": "https://drive.usercontent.google.com/download?id=19J_SaJGQ3g7GhIHrswTuzzbx0JITtn_j"
        },
    ])

    response = model.invoke([message])
    pprint(response.content)


if __name__ == "__main__":
    # analyze_image_example()
    # transcribe_audio_example()
    # analyze_pdf_example()
    combined_multimodal_example()
    # compare_images_example()
