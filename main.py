from src.web_rag_application.web_rag_application_agent import agent_executor

config = {"configurable": {"thread_id": "def234"}}

input_message = (
    "Какой стандартный метод декомпозиции задач? используй retriever для получения данных\n\n"
    "Как только получишь ответ, найди распространенные расширения этого метода."
)

for event in agent_executor.stream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="values",
        config=config,
):
    event["messages"][-1].pretty_print()
