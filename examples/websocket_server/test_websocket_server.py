import asyncio
import pytest
import time
from websocket_server import WebSocketServer
from websockets.sync.client import connect
@pytest.mark.asyncio
async def test_WebSocketServer_conn():
    server = WebSocketServer()
    await server.start_with_catch()
    secs = 20
    print(f"sleep for {secs} seconds")
    time.sleep(secs)
    print("slept for {secs} seconds")
    ws = connect("ws://localhost:8765")
    ws.send("hello from client")
    response = ws.recv()
    print(f"response from server: {response}")
    await server.stop()
    print("test complete")