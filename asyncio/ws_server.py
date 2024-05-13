import asyncio
import os
import sys

import websockets
from task_handler import handle_request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


async def server(websocket):
    try:
        async for message in websocket:
            response = await handle_request(message)
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedOK:
        print('Client has left the building')
    except Exception as e:
        print(f'Something went wrong: {e}')


start_server = websockets.serve(server, config.server_host, config.server_port, ping_timeout=config.server_timeout_sec)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()