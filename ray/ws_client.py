import asyncio
import os
import sys

import websockets
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


NUM_CLIENTS = config.client_num_client
TASKS = config.client_tasks
TASKS_PER_CLIENT = len(TASKS)
URI = f'ws://{config.server_host}:{config.server_port}'


async def client(uri, client_id):
    start_time = time.time()

    async with websockets.connect(uri, ping_timeout=config.server_timeout_sec) as websocket:
        for task in range(TASKS_PER_CLIENT):
            await websocket.send(TASKS[task])
            response = await websocket.recv()

    end_time = time.time()

    print(f"Cliente {client_id} tardó {round(end_time - start_time, 2)} [s] en resolver todas sus tareas")


async def stress_test():
    tasks = []
    for i in range(NUM_CLIENTS):
        tasks.append(client(URI, i + 1))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(stress_test())




