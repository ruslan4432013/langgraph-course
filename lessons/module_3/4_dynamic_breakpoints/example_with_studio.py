import asyncio


async def main():
    from langgraph_sdk import get_client

    # URL локального сервера разработки
    URL = "http://127.0.0.1:2024"
    client = get_client(url=URL)

    # Поиск всех размещенных графов
    assistants = await client.assistants.search()
    thread = await client.threads.create()
    input_dict = {"input": "hello world"}

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="dynamic_breakpoints",
            input=input_dict,
            stream_mode="values",
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

    current_state = await client.threads.get_state(thread['thread_id'])
    print(current_state)
    await client.threads.update_state(thread['thread_id'], {"input": "hi!"})

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="dynamic_breakpoints",
            input=None,
            stream_mode="values",
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

    current_state = await client.threads.get_state(thread['thread_id'])
    print(current_state)


if __name__ == '__main__':
    asyncio.run(main())