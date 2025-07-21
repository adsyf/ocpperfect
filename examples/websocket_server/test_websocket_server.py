import asyncio
import pytest
import logging
import time
from websocket_server import WebSocketServer
from websockets.sync.client import connect
logging.basicConfig(level=logging.INFO)

@pytest.fixture
async def websocket_server():
    logging.info("run fixture")

server = WebSocketServer()
# asyncio.run(server.start_with_catch())
logging.info("try start server")
await server.start()

@pytest.mark.asyncio
async def test_websocket_server_conn():
    logging.info("test_websocket_server_conn")

    logging.info("sleep 0.1 sec")
    await asyncio.sleep(0.1)
    #secs = 20
    #print(f"sleep for {secs} seconds")
    #time.sleep(secs)
    #print("slept for {secs} seconds")
    try:
        logging.info("try client connect")
        ws = connect("ws://localhost:8765")
        ws.send("hello from client")
        response = ws.recv()
        logging.info(f"response from server: {response}")
    finally:
        logging.info("finally stop server")
        await server.stop()
    print("test complete")