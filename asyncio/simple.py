import asyncio

async def say_hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")

if __name__ == "__main__":
    asyncio.run(say_hello())