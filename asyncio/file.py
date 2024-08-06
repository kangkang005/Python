import asyncio
import aiofiles

async def read_file_async(file_path):
    async with aiofiles.open(file_path, 'r') as file:
        data = await file.read()
        return data


async def write_file_async(file_path, data):
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(data)

async def main():
    data = await read_file_async('example.txt')
    await write_file_async('example_copy.txt', data)

asyncio.run(main())