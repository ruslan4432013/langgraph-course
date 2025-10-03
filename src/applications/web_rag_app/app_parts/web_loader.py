import bs4
from langchain_community.document_loaders import WebBaseLoader

# Оставляем только post-title, headers, and content from the full HTML.
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()

if __name__ == "__main__":
    print(docs[0].page_content[:200])
    print(len(docs))
    print(f"Количество симовлов: {len(docs[0].page_content)}")
