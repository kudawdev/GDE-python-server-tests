import asyncio
import os
import sys

import websockets
import random
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)

TASKS = 10


async def send_request(i):
    rand_num = random.randint(1, 5)
    async with websockets.connect(f'ws://{config.server_host}:{config.server_port}') as websocket:
        start_time = time.time()
        await websocket.send(str(rand_num))
        response = await websocket.recv()
        end_time = time.time()
        total_time = end_time - start_time
        print(f"La tarea {i} de {rand_num} [s] tardó {int(total_time)} [s] en completarse")


async def send_requests():
    tasks = []
    for i in range(TASKS):
        task = send_request(i)
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(send_requests())
