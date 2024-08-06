# @web: https://blog.csdn.net/qq_44159028/article/details/139449244
import asyncio
import aiohttp
from tqdm.asyncio import tqdm  # 导入 tqdm 的异步版本

max_retries = 1  # 设置最大重试次数
alive_code = [200, 301, 302, 303, 304, 401, 403]
results = []
lock = asyncio.Lock()

async def dirfuzzMain(session, sem, path, progress_bar, retries=0):
    async with sem:
        try:
            async with session.get(
                path,
                proxy='http://127.0.0.1:8080',
                timeout=aiohttp.ClientTimeout(total=3)
            ) as response:
                code = response.status
                if code in alive_code:
                    tqdm.write(path + " " + str(code))
                    progress_bar.update()
                    async with lock:
                        results.append((path, code))
                else:
                    progress_bar.update()

        except Exception as e:
            if retries < max_retries:
                # 递归调用自身，增加重试次数
                await asyncio.sleep(0.5)  # 可以添加等待时间，避免过于频繁的请求
                return await dirfuzzMain(session, sem, path, progress_bar, retries + 1)
            else:
                progress_bar.update()

async def main():
    url = "http://192.168.59.132"
    dicc =  ["1.txt", "test.php", "common.inc.php", "info.php"]
    dicc =  ["1.txt", "test.php"]

    sem = asyncio.Semaphore(3)
    connector = aiohttp.TCPConnector(ssl=False)
    with tqdm(total=len(dicc), desc="Requesting", bar_format='{desc}: {percentage:.0f}% ({n_fmt}/{total_fmt}) {elapsed}') as progress_bar: 
        async with aiohttp.ClientSession(connector=connector) as session:
            # 创建一个任务列表
            tasks = []
            # 为每个URL创建一个fetch任务
            for path in dicc:
                path = url + "/" + path
                task = asyncio.create_task(dirfuzzMain(session, sem, path, progress_bar))
                tasks.append(task)
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()      #获取当前的事件循环
    loop.run_until_complete(main()) #启动事件循环并运行给定的协程，直到该协程完成。