import asyncio
from urllib import response
import websockets
import logging
from config import *

class WebSocketServer:
    def __init__(self):
        self.clients = set()
        self.server = None
        self.cfg = get_env_config()
        self.logger = logging.getLogger(__name__)

    async def _handle(self,websocket):
        self.logger.info("client connected")
        async for message in websocket:
            path = websocket.request.path.strip("/")
            self.logger.info(f"websocket path: {path}")
            if path.startswith(self.cfg.websocket.echo_path):
                self.logger.info(f"received message: {message}")
                response = message
                await websocket.send(response)
                self.logger.info(f"sent message: {response}")
            else:
                self.logger.info("doing nothing as not echo server")

    async def start_server(self):
        self.logger.info("starting server")
        self.server = await websockets.serve(self._handle, self.cfg.websocket.host, self.cfg.websocket.port)
        self.logger.info("server started")
        await asyncio.sleep(0.1)
        self.logger.info("finished sleep")
        return self.server, self.logger

async def main():
    websocket_server = WebSocketServer()
    server = await websocket_server.start_server()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())