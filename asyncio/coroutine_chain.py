import asyncio

# pipeline

async def coroutine1(data):
    print(f"Coroutine1: {data}")
    await asyncio.sleep(0.1)
    return data * 2


async def coroutine2(data):
    print(f"Coroutine2: {data}")
    await asyncio.sleep(0.1)
    return data ** 2


async def main():
    data = 1
    coroutines = [coroutine1, coroutine2]
    for coroutine in coroutines:
        data = await coroutine(data)
    print(f"Final result: {data}")


asyncio.run(main())