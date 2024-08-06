# @web: https://www.cnblogs.com/Amd794/p/18162269
import asyncio
import aiohttp
import time

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

@timing_decorator
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


@timing_decorator
async def main():
    urls = ["http://example.com/page1", "http://example.com/page2", "http://example.com/page3"]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


asyncio.run(main())