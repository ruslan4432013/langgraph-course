import asyncio

from langchain_core.messages import HumanMessage

from agent import graph


# async def main():
#     config = {"configurable": {"thread_id": "3"}}
#     input_message = HumanMessage(content="Расскажи мне о команде NFL '49ers'")
#     async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
#         print(f"Узел: {event['metadata'].get('langgraph_node', '')}. Тип: {event['event']}. Название: {event['name']}")
#
#
# asyncio.run(main())


# async def main_2():
#     node_to_stream = 'conversation'
#     config = {"configurable": {"thread_id": "4"}}
#     input_message = HumanMessage(content="Расскажи мне о команде NFL '49ers'")
#
#     async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
#         # Получаем токены чат-модели из определенного узла
#         if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == node_to_stream:
#             print(event["data"])
#
# asyncio.run(main_2())


async def main_3():
    node_to_stream = 'conversation'
    config = {"configurable": {"thread_id": "5"}}
    input_message = HumanMessage(content="Расскажи мне о команде NFL '49ers'")

    async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
        # Получаем токены чат-модели из определенного узла
        if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == node_to_stream:
            data = event["data"]
            print(data["chunk"].content, end="")


asyncio.run(main_3())
