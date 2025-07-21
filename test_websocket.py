import sys

import pytest
import websockets
import logging
from server import WebSocketServer
import sys
from config import *


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)],
                    force=True
                    )
os.environ["ENV"] = "dev"
cfg = get_env_config()


@pytest.fixture
async def websocket_server():
    websocket_server = WebSocketServer()
    server,logger = await websocket_server.start_server()
    logger.setLevel(logging.INFO)
    yield server
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_websocket_connection(websocket_server):
    uri = cfg.websocket.get_url()
    async with websockets.connect(uri) as websocket:
        assert websocket.state.name == 'OPEN'

@pytest.mark.asyncio
async def test_generic_websocket_echo_msg(websocket_server):
    uri = cfg.websocket.get_url() + "/" + cfg.websocket.echo_path
    msg = "hello"
    async with websockets.connect(uri) as websocket:
        await websocket.send(msg)
        rsp = await websocket.recv()
        assert rsp == msg