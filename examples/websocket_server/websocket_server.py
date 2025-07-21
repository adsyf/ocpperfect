import asyncio
import time

import websockets
import logging
logging.basicConfig(level=logging.INFO)
class WebSocketServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.server = None
        self._server_task = None
    async def _handler(self, websocket):
        logging.info(f"start handler")
        try:
            async for message in websocket:
                await websocket.send(f"got message {message}")
                logging.info(f"message sent")
        except websockets.exceptions.ConnectionClosedError:
            logging.info("websocket connection closed exception raised")

    async def start(self):
        logging.info(f"starting server")
        self.server = await websockets.serve(self._handler, self.host, self.port)
        logging.info(f"server started at ws://{self.host}:{self.port}")
        self._server_task = asyncio.create_task(self.server.wait_closed())
        logging.info(f"server started as task")

    async def stop(self,timeout: float = 5.0):
        if self.server:
            logging.info(f"found server")
            self.server.close()
            try:
                await asyncio.wait_for(self.server.wait_closed(), timeout=timeout)
                logging.info(f"server shutdown cleanly")
            except asyncio.TimeoutError:
                logging.info(f"server shutdown timed out")
            logging.info(f"server closed")
        if self._server_task:
            logging.info(f"found task")
            self._server_task.cancel()
            try:
                await self._server_task
                logging.info(f"task cancelled cleanly")
            except asyncio.CancelledError:
                logging.info(f"task cancelled with cancel error")
            logging.info(f"task cancelled")

    async def stop_and_log(self,initial_exception):
        await self.stop()
        logging.info(f"server stopped after {initial_exception}")

    async def start_with_catch_forever(self):
        await self.start()
        try:
            await asyncio.Future()
        except asyncio.exceptions.CancelledError:
            logging.info("CancelledError received. shutting down...")
            await self.stop_and_log( "CancelledError")
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt received. shutting down...")
            await self.stop_and_log( "KeyboardInterrupt")
        except Exception as e:
            logging.error(f"Unexpected server shutdown error: {e}")
            await self.stop_and_log( "Exception")


if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start_with_catch_forever())

