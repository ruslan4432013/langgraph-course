import asyncio

from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client

URL = "http://127.0.0.1:2024"
client = get_client(url=URL)


async def main():
    initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}
    thread = await client.threads.create()

    async for chunk in client.runs.stream(
            thread["thread_id"],
            "agent",
            input=initial_input,
            stream_mode="values",
            interrupt_before=["assistant"],
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        if not chunk.data:
            continue
        messages = chunk.data.get('messages', [])

        if messages:
            print(messages[-1])
        print("-" * 50)

    current_state = await client.threads.get_state(thread['thread_id'])
    print(f'{current_state=}')

    last_message = current_state['values']['messages'][-1]
    print(f'{last_message=}')

    last_message['content'] = "Нет, умножь 3 и 3!"
    print(f'{last_message=}')

    await client.threads.update_state(thread['thread_id'], {"messages": last_message})

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=None,
            stream_mode="values",
            interrupt_before=["assistant"],
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        if not chunk.data:
            continue
        messages = chunk.data.get('messages', [])
        if messages:
            print(messages[-1])
        print("-" * 50)

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=None,
            stream_mode="values",
            interrupt_before=["assistant"],
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        if not chunk.data:
            continue
        messages = chunk.data.get('messages', [])
        if messages:
            print(messages[-1])
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
