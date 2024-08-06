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

async def process_data(data):
    print(f"Processing data: {data}")
    await asyncio.sleep(0.1)
    return data.upper()


@timing_decorator
async def main():
    data_stream = ["data1", "data2", "data3"]
    tasks = [process_data(data) for data in data_stream]
    processed_data = await asyncio.gather(*tasks)
    print(f"Processed data: {processed_data}")


asyncio.run(main())