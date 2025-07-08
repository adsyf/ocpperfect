import asyncio
import websockets

# Function to handle the chat client
async def chat():
    async with websockets.connect('ws://localhost:9000') as websocket:
        while True:
            message = input("enter message: ")
            await websocket.send(message)
            response = await websocket.recv()
            print(f"response from server: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(chat())