import uuid

from langchain_core.documents import Document

document = Document(
    id=uuid.uuid4(),
    page_content="Hello, world!",
    metadata={"source": "https://example.com"}
)

print(document.__repr__())
