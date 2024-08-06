# @web: https://blog.csdn.net/qq_43629857/article/details/133389165
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor, Executor

def run_on_executor(executor: Executor = None, background: bool = False):
    """
    异步装饰器
    - 支持同步函数使用 executor 加速
    - 异步函数和同步函数都可以使用 `await` 语法等待返回结果
    - 异步函数和同步函数都支持后台任务，无需等待
    Args:
        executor: 函数执行器, 装饰同步函数的时候使用
        background: 是否后台执行，默认False

    Returns:
    """

    def _run_on_executor(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if background:
                return asyncio.create_task(func(*args, **kwargs))
            else:
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            task_func = functools.partial(func, *args, **kwargs)    # 支持关键字参数
            return loop.run_in_executor(executor, task_func)

        # 异步函数判断
        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return wrapper_func

    return _run_on_executor

############# demo ################
import time
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

thread_executor = ThreadPoolExecutor(max_workers=3)


@run_on_executor(background=True)
async def async_func_bg_task():
    logger.debug("async_func_bg_task start")
    await asyncio.sleep(1)
    logger.debug("async_func_bg_task running")
    await asyncio.sleep(1)
    logger.debug("async_func_bg_task end")
    return "async_func_bg_task ret end"


@run_on_executor()
async def async_func():
    logger.debug("async_func start")
    await asyncio.sleep(1)
    logger.debug("async_func running")
    await asyncio.sleep(1)
    return "async_func ret end"


@run_on_executor(background=True, executor=thread_executor)
def sync_func_bg_task():
    logger.debug("sync_func_bg_task start")
    time.sleep(1)
    logger.debug("sync_func_bg_task running")
    time.sleep(1)
    logger.debug("sync_func_bg_task end")
    return "sync_func_bg_task end"


@run_on_executor()
def sync_func():
    logger.debug("sync_func start")
    time.sleep(1)
    logger.debug("sync_func running")
    time.sleep(1)
    return "sync_func ret end"


async def main():
    ret = await async_func()
    logger.debug(ret)

    async_bg_task = await async_func_bg_task()
    logger.debug(f"async bg task {async_bg_task}")
    logger.debug("async_func_bg_task 等待后台执行中")

    loop = asyncio.get_event_loop()
    for i in range(3):
        loop.create_task(async_func())

    ret = await sync_func()
    logger.debug(ret)

    sync_bg_task = sync_func_bg_task()
    logger.debug(f"sync bg task {sync_bg_task}")
    logger.debug("sync_func_bg_task 等待后台执行")

    await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())