import base64
from pprint import pprint

from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.settings import settings, current_file

model = ChatOpenAI(
    model="gpt-5.2",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.1,
    max_retries=2,
    base_url="https://api.proxyapi.ru/openai/v1"
)

pdf_path = current_file.parent / "resources" / "rental.pdf"

# 1. PDF-документ по URL (через HumanMessage)
message_pdf_url = HumanMessage(
    content=[
        {"type": "text", "text": "Опишите содержимое этого документа."},
        {
            "type": "file",
            "url": "https://example.com/document.pdf",
            "mime_type": "application/pdf",
        },
    ]
)


# 2. PDF-документ из base64
# ВАЖНО: OpenAI требует указания имени файла (filename) для PDF-документов.
def get_pdf_message_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return HumanMessage(
        content=[
            {"type": "text", "text": "Кратко изложите основные тезисы документа."},
            {
                "type": "file",
                "base64": pdf_data,
                "mime_type": "application/pdf",
                "filename": "document.pdf",  # Обязательно для OpenAI
            },
        ]
    )


# 3. Файл по File ID
message_file_id = HumanMessage(
    content=[
        {"type": "text", "text": "Проанализируйте этот документ."},
        {"type": "file", "file_id": "file-abc123"},
    ]
)

# 4. Текстовые документы (PlainTextContentBlock)
# Для текстовых файлов (.txt, .md) используется тип text-plain
message_text_plain = HumanMessage(
    content=[
        {"type": "text", "text": "Проанализируйте этот текст."},
        {
            "type": "text-plain",
            "text": "Содержимое текстового документа...",
            "mime_type": "text/markdown",
        },
    ]
)

if __name__ == "__main__":
    # Пример с base64
    print("--- Отправка PDF (Base64) ---")
    pdf_message = get_pdf_message_base64(pdf_path)
    response = model.invoke([pdf_message])
    pprint(response.content)
