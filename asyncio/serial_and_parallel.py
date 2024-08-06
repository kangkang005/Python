import asyncio
import time

def timing_decorator(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper

@timing_decorator
async def fun1():
    print("fun1 begin")
    await asyncio.sleep(1)
    print("fun1 finish")

@timing_decorator
async def fun2():
    print("fun2 begin")
    await asyncio.sleep(1)
    print("fun2 finish")

@timing_decorator
async def serial():
    print("######## serial ##########")
    await fun1()
    await fun2()

@timing_decorator
async def parallel():
    print("######## parallel ##########")
    task = [
        fun1(),
        fun2(),
    ]
    await asyncio.gather(*task)

asyncio.run(serial())
asyncio.run(parallel())