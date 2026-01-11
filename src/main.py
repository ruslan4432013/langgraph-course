import asyncio
import pprint

from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client

# URL локального сервера
URL = "http://127.0.0.1:2024"
client = get_client(url=URL)


async def main():
    # Создаем тред для отслеживания состояния
    thread = await client.threads.create()

    # Входные данные
    input_messages = {"messages": [HumanMessage(content="Умножь 3 на 2.")]}
    assistants = await client.assistants.search()
    result = [*filter(lambda x: x['graph_id'] == 'agent', assistants)]
    agent = None
    if result:
        agent = result[0]

    if not agent:
        return


    # Потоковая передача
    async for chunk in client.runs.stream(
            thread['thread_id'],
            agent['graph_id'],
            input=input_messages,
            stream_mode="values",
    ):
        if chunk.data and chunk.event != "metadata":
            print(chunk.data['messages'][-1])


if __name__ == "__main__":
    asyncio.run(main())
