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
            assistant_id="agent",
            input=initial_input,
            stream_mode="values",
            interrupt_before=["tools"],
    ):
        print(f"Получено новое событие типа: {chunk.event}...")
        if not chunk.data:
            return
        messages = chunk.data.get('messages', [])
        if messages:
            print(messages[-1])
        print("-" * 50)

    ### 2-я часть
    user_approval = input("Вы хотите вызвать инструмент? (да/нет): ")

    if user_approval.lower() == 'да':
        async for chunk in client.runs.stream(
                thread["thread_id"],
                "agent",
                input=None,
                stream_mode="values",
                interrupt_before=["tools"],
        ):
            print(f"Получено новое событие типа: {chunk.event}...")
            if not chunk.data:
                return
            messages = chunk.data.get('messages', [])
            if messages:
                print(messages[-1])
            print("-" * 50)

    else:
        print('Пользователь отменил операцию')


if __name__ == "__main__":
    asyncio.run(main())