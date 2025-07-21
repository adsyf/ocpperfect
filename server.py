import asyncio
from urllib import response
import websockets
import logging

logger = logging.getLogger(__name__)

async def _handle(websocket):
    logger.info("client connected")
    async for message in websocket:
        logging.info(f"received message: {message}")
        response = "got " + message
        await websocket.send(response)
        logging.info(f"sent message: {response}")

async def start_server():
    logger.info("starting server")
    server = await websockets.serve(_handle, "localhost", 8765)
    logger.info("server started")
    await asyncio.sleep(0.1)
    logger.info("finished sleep")
    return server
