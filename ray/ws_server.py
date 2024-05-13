import asyncio
import os
import sys

import websockets
from task_handler import handle_request
import ray

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)

ray.init()


async def server(websocket, path):
    async for request in websocket:
        response_ref = handle_request.remote(request)
        response = ray.get(response_ref)
        await websocket.send(response)


start_server = websockets.serve(server, config.server_host, config.server_port, ping_timeout=config.server_timeout_sec)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()