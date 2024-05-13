import asyncio
import multiprocessing
import os
import sys

import websockets
from task_handler import fib, io_bound_task, cpu_bound_task

'''
Cambio en la estructura vs los ejemplos anteriores:
Se esta usando asyncio para manejar concurrentemente las solicitudes de WebSocket y multiprocessing para ejecutar 
tareas en paralelo en múltiples cores (procesos).
'''

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


def handle_io_message(queue):
    # print("Handling IO message")
    result = io_bound_task(config.task_setting_large_file_name)
    queue.put(result)


def handle_fib_message(queue):
    # print("Handling CPU message")
    result = fib(config.task_setting_fibonacci_limit)
    queue.put(result)


def handle_cpu_message(queue):
    # print("Handling CPU-IO message")
    result = cpu_bound_task()
    queue.put(result)


async def handle_websocket_request(websocket, path, pool, queue):
    async for message in websocket:
        # print("Message received: ", message)
        if message == 'fib':
            pool.apply_async(handle_fib_message, (queue,))
        elif message == 'io':
            pool.apply_async(handle_io_message, (queue,))
        elif message == 'cpu':
            pool.apply_async(handle_cpu_message, (queue,))
        result = queue.get()
        # print("Sending: ", result)
        await websocket.send(str(result))


def print_cpu_count():
    cpu_count = multiprocessing.cpu_count()
    print(f"Total CPU Cores: {cpu_count}")


def main():
    queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(processes=config.other_multiprocessing_processes)
    start_server = websockets.serve(lambda ws, path: handle_websocket_request(ws, path, pool, queue), config.server_host, config.server_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started")
    print_cpu_count()
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
