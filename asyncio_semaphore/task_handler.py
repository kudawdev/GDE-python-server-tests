import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


semaphore = asyncio.Semaphore(config.other_asyn_semaphore)


async def handle_request(message):
    async with semaphore:
        num_seconds = int(message)
        print(f"Solicitud recibida, esperando {num_seconds} segundos...")
        await asyncio.sleep(num_seconds)
        return "Request done"