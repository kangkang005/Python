from pprint import *
import aiohttp
import datetime
import asyncio

def time_log(func):
    async def wrap(*args, **kwargs):
        print(f'now: {datetime.datetime.now()}, begin...')
        result = await func(*args, **kwargs)
        print(f'now: {datetime.datetime.now()}, end')
        return result
    return wrap

@time_log
async def get(n):
    async with aiohttp.ClientSession() as client:
        resp   = await client.get(f'http://httpbin.org/delay/{n}')
        result = await resp.json()
    pprint(result, indent=2)

asyncio.run(get(3))