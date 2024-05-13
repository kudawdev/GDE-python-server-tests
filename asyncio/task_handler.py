import asyncio
import os
import sys

import aiofiles


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


async def handle_request(task_name):
    if task_name == "cpu":
        result = await cpu_bound_task()
    elif task_name == "io":
        result = await io_bound_task()
    elif task_name == "fib":
        result = await fib(config.task_setting_fibonacci_limit)
    else:
        result = "Task no found"

    return str(result)


async def cpu_bound_task():
    result = 0
    for i in range(10 ** 6):
        result += i
    return result


async def fib(size):
    a, b = 0, 1
    for _ in range(size):
        await asyncio.sleep(0)  # desbloqueo del evento async
        a, b = b, a + b
    return a


async def io_bound_task(filename):
    content_to_write = 'a' * 10 ** 6
    async with aiofiles.open(f'files/{config.task_setting_large_file_name}', 'w') as f:
        await f.write(content_to_write)
    async with aiofiles.open(f'files/{config.task_setting_large_file_name}', 'r') as f:
        content = await f.read()
    # os.remove(LARGE_FILE)
    return len(content)
