import os

from pydantic import BaseModel
import pathlib
import yaml
#https://www.youtube.com/watch?v=ZvcZDxS_mYE&t=167s
#https://medium.com/@jonathan_b/a-simple-guide-to-configure-your-python-project-with-pydantic-and-a-yaml-file-bef76888f366
cwd = pathlib.Path(__file__).parent
config_file = cwd / "config.yaml"

class QueueConfig(BaseModel):
    queue_name: str = "task_queue"
    host: str = "localhost"
    port: int = 5672
    management_port: int = 15672
    durable: bool = True
    auto_ack: bool = False

class WebsocketConfig(BaseModel):
    host: str = "localhost"
    port: int = 9000
    def get_url(self):
        return f"ws://{self.host}:{self.port}"

class EnvConfig(BaseModel):
    queue: QueueConfig
    websocket: WebsocketConfig



def get_env_config(non_file_yaml = None):
    if non_file_yaml is None:
        try:
            with open(config_file) as f:
                _yaml_obj = yaml.safe_load(f)
        except FileNotFoundError as error:
            message = "error: yml config file not found."
            raise FileNotFoundError(error, message) from error
    else:
        _yaml_obj = yaml.safe_load(non_file_yaml)
    env_config_dict = _yaml_obj[os.getenv("ENV", "dev")]
    return EnvConfig(**env_config_dict)


if __name__ == "__main__":
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

    env = get_env_config()
    print(env)


