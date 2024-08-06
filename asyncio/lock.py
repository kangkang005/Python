import asyncio

shared_resource = 0
lock = asyncio.Lock()


async def update_shared_resource():
    global shared_resource
    async with lock:
        shared_resource += 1


async def main():
    tasks = [update_shared_resource() for _ in range(10)]
    await asyncio.gather(*tasks)
    print(f"Final shared resource value: {shared_resource}")


asyncio.run(main())