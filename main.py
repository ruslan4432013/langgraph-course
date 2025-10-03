from src.applications.web_rag_app.web_rag_app_with_analyze import graph

response = graph.invoke({"question": "Что написано в конце поста о Task Decomposition?"})
print(response["answer"])
