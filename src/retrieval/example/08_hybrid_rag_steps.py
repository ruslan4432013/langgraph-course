# https://python.langchain.com/docs/how_to/agentic_rag_self_correction/

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# Query enhancement
enhance_prompt = PromptTemplate.from_template("Улучши запрос: {query}")
enhancer = enhance_prompt | llm

# Retrieval validation
validate_prompt = PromptTemplate.from_template("Релевантны ли docs к {query}? {docs}")
validator = validate_prompt | llm

enhanced_query = enhancer.invoke({"query": "оригинальный запрос"})
print(enhanced_query.content)