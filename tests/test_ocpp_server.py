from ocpperfect import ocpp_server as ocpp_server
from ocpperfect import config as config
from websockets.sync.client import connect
from ocpperfect import config as config
cfg = config.get_env_config()

def test_starts():
    ocpp_server.main()
    websocket = connect(cfg.websocket.get_url())
    assert websocket is not None


