import asyncio

from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client

client = get_client(url="http://127.0.0.1:2024")


async def main():
    initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}
    thread = await client.threads.create()

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=initial_input,
            stream_mode="updates",
    ):
        if chunk.data:
            assistant_node = chunk.data.get('assistant', {}).get('messages', [])
            tool_node = chunk.data.get('tools', {}).get('messages', [])
            if assistant_node:
                print("-" * 20 + "Assistant Node" + "-" * 20)
                print(assistant_node[-1])
            elif tool_node:
                print("-" * 20 + "Tools Node" + "-" * 20)
                print(tool_node[-1])

    states = await client.threads.get_history(thread['thread_id'])
    to_replay = states[-2]
    print(to_replay)

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=None,
            stream_mode="values",
            checkpoint_id=to_replay['checkpoint_id']
    ):
        print(f"Получен ивент: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=None,
            stream_mode="updates",
            checkpoint_id=to_replay['checkpoint_id']
    ):
        if chunk.data:
            assistant_node = chunk.data.get('assistant', {}).get('messages', [])
            tool_node = chunk.data.get('tools', {}).get('messages', [])
            if assistant_node:
                print("-" * 20 + "Assistant Node" + "-" * 20)
                print(assistant_node[-1])
            elif tool_node:
                print("-" * 20 + "Tools Node" + "-" * 20)
                print(tool_node[-1])

    initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}
    thread = await client.threads.create()

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=initial_input,
            stream_mode="updates",
    ):
        if chunk.data:
            assisant_node = chunk.data.get('assistant', {}).get('messages', [])
            tool_node = chunk.data.get('tools', {}).get('messages', [])
            if assisant_node:
                print("-" * 20 + "Assistant Node" + "-" * 20)
                print(assisant_node[-1])
            elif tool_node:
                print("-" * 20 + "Tools Node" + "-" * 20)
                print(tool_node[-1])

    states = await client.threads.get_history(thread['thread_id'])
    to_fork = states[-2]
    print(to_fork['values'])
    print(to_fork['values']['messages'][0]['id'])
    print(to_fork['next'])
    print(to_fork['checkpoint_id'])

    forked_input = {"messages": HumanMessage(content="Умножь 3 и 5",
                                             id=to_fork['values']['messages'][0]['id'])}
    # Обновление состояния
    forked_config = await client.threads.update_state(
        thread["thread_id"],
        forked_input,
        checkpoint_id=to_fork['checkpoint_id']
    )

    async for chunk in client.runs.stream(
            thread["thread_id"],
            assistant_id="agent",
            input=None,
            stream_mode="updates",
            checkpoint_id=forked_config['checkpoint_id']
    ):
        if chunk.data:
            assisant_node = chunk.data.get('assistant', {}).get('messages', [])
            tool_node = chunk.data.get('tools', {}).get('messages', [])
            if assisant_node:
                print("-" * 20 + "Assistant Node" + "-" * 20)
                print(assisant_node[-1])
            elif tool_node:
                print("-" * 20 + "Tools Node" + "-" * 20)
                print(tool_node[-1])


if __name__ == "__main__":
    asyncio.run(main())