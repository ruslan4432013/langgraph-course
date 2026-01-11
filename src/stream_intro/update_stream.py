from langchain_core.messages import HumanMessage

from src.stream_intro.agent import graph

# Создаем конфигурацию потока
config = {"configurable": {"thread_id": "1"}}

# # Начинаем диалог
# for chunk in graph.stream({"messages": [HumanMessage(content="Привет! Я Ланс")]}, config, stream_mode="updates"):
#     print(chunk)


# Начинаем диалог
for chunk in graph.stream({"messages": [HumanMessage(content="Привет! Я Ланс")]}, config, stream_mode="updates"):
    for key, value in chunk.items():
        if 'messages' in value:
            print(key)
            value["messages"].pretty_print()
