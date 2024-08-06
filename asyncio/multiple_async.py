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

async def say_hello():
    print("hello")
    await asyncio.sleep(2)
    print("world")
    return "finish"

# 1.直接调用协程
@timing_decorator
async def main():
    tasks = [
        say_hello(),
        say_hello(),
        say_hello()
    ]
    results = await asyncio.gather(*tasks)
    print(results)

# 2. asyncio.create_task()
@timing_decorator
async def create():
    tasks = []
    for _ in range(3):
        task = asyncio.create_task(say_hello())
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(create())