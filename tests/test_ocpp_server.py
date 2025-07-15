import os
from ocpperfect import ocpp_server, config
from websockets.sync.client import connect
import pytest
#@pytest.mark.skip(reason="not running")
def test_starts():
    os.environ["ENV"] = "dev"
    env_config = config.get_env_config()
    print("try start ocpp server")
    server = ocpp_server.OCPPServer()
    server.start_ocpp_server()
    print("started ocpp server")
    websocket = connect(env_config.websocket.get_url())
    assert websocket is not None


