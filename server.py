import asyncio
from urllib import response
import websockets
import logging
from config import *

logger = logging.getLogger(__name__)
class WebSocketServer:
    def __init__(self):
        self.clients = set()
        self.server = None
        self.cfg = get_env_config()

    async def _handle(self,websocket):
        logger.info("client connected")
        async for message in websocket:
            logging.info(f"received message: {message}")
            response = "got " + message
            await websocket.send(response)
            logging.info(f"sent message: {response}")

    async def start_server(self):
        logger.info("starting server")
        server = await websockets.serve(self._handle, self.cfg.websocket.host, self.cfg.websocket.port)
        logger.info("server started")
        await asyncio.sleep(0.1)
        logger.info("finished sleep")
        return server
