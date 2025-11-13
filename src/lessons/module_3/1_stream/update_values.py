from langchain_core.messages import HumanMessage

from agent import graph

# Начинаем диалог снова
config = {"configurable": {"thread_id": "2"}}

# Начинаем диалог
input_message = HumanMessage(content="Привет! Я Ланс")
for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    print("=" * 25 + "Event" + "=" * 25)
    print(event)
    print("=" * 25 + "Event" + "=" * 25)
    for m in event['messages']:
        m.pretty_print()
    print("---"*25)