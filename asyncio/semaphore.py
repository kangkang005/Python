import asyncio, time

def timing_decorator(func):
    async def wrapper(*args, **kwargs):
        print("# before")
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        print("# after")
        return result
    return wrapper

async def say_hello(sem):
    async with sem:
        print("hello")
        await asyncio.sleep(2)
        print("world")

@timing_decorator
async def main():
    sem = asyncio.Semaphore(2)  # 限制同时运行的携程数量最大为2
    tasks = []
    for _ in range(10):
        task = asyncio.create_task(say_hello(sem))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())