import asyncio
import websockets
import config

cfg = config.get_env_config()
# Function to handle the chat client
async def listen():
    async with websockets.connect(cfg.websocket.get_url()) as websocket:
        while True:
            response = await websocket.recv()
            print(f"response from server: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(listen())