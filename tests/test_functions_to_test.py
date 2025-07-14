import os

import ocpperfect.functions_to_test as functions_to_test
from ocpperfect import config as config


def test_add():
    assert functions_to_test.add(1,2) == 3

def test_conf():
    my_yaml = """
test:
  queue:
    host: 'test-queue-host'
  websocket:
    host: 'test-websocket-host'
dev:
  queue: {}
  websocket: {}
"""
    os.environ["ENV"] = "test"
    env_config = config.get_env_config(my_yaml)
    print(env_config)
    assert env_config.queue.host == "test-queue-host"

def test_conf_get_ws_url():
    my_yaml = """
    test:
      queue:
        host: 'test-queue-host'
      websocket:
        host: 'test-websocket-host'
        port: 9000
    dev:
      queue: {}
      websocket: {}
    """
    os.environ["ENV"] = "test"
    env_config = config.get_env_config(my_yaml)
    assert env_config.websocket.get_url() == "ws://test-websocket-host:9000"