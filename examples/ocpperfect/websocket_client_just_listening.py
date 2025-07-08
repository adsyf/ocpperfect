import asyncio
import websockets

# Function to handle the chat client
async def listen():
    async with websockets.connect('ws://localhost:9000') as websocket:
        while True:
            response = await websocket.recv()
            print(f"response from server: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(listen())