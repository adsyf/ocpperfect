import sys

import pytest
import websockets
import logging
from server import WebSocketServer, logger
import sys
from config import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)],
                    force=True
                    )

logger.setLevel(logging.INFO)
os.environ["ENV"] = "dev"
cfg = get_env_config()


@pytest.fixture
async def websocket_server():
    websocket_server = WebSocketServer()
    server = await websocket_server.start_server()
    yield server
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_websocket_connection(websocket_server):
    #uri = "ws://localhost:8765"
    uri = cfg.websocket.get_url()
    async with websockets.connect(uri) as websocket:
        assert websocket.state.name == 'OPEN'
