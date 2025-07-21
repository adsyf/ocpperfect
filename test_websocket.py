import sys

import pytest
import websockets
import logging
from server import WebSocketServer, logger
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)],
                    force=True
                    )

logger.setLevel(logging.INFO)

@pytest.fixture
async def websocket_server():
    websocket_server = WebSocketServer()
    server = await websocket_server.start_server()
    yield server
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_websocket_connection(websocket_server):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        assert websocket.state.name == 'OPEN'
