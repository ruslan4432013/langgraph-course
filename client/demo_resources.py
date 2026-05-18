"""Демонстрация загрузки ресурсов."""
import asyncio

from client._shared import client


async def demo_resources():
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РЕСУРСОВ")
    print("=" * 50)

    # blobs = await client.get_resources("todo")
    # for blob in blobs:
    #     print(f"URI: {blob.metadata['uri']}")
    #     print(f"MIME: {blob.mimetype}")
    #     print(f"Содержимое: {blob.as_string()}\n")

    blobs = await client.get_resources("todo", uris=['to-do://tasks/work'])
    for blob in blobs:
        print(f"URI: {blob.metadata['uri']}")
        print(f"MIME: {blob.mimetype}")
        print(f"Содержимое: {blob.as_string()}\n")


if __name__ == "__main__":
    asyncio.run(demo_resources())
