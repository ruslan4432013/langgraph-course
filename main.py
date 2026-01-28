from src.applications.web_rag_app.web_rag_app_with_analyze import graph

response = graph.invoke({"question": "Расскажи о Task Decomposition"})
print(response["answer"])
