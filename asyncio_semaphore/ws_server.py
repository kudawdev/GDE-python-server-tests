import asyncio
import os
import sys

import websockets
from task_handler import handle_request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


async def server(websocket, path):
    async for message in websocket:
        response = await handle_request(message)
        await websocket.send(response)


start_server = websockets.serve(server, config.server_host, config.server_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()