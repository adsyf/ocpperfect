
import websockets
from websockets.sync.client import connect

# Function to handle the chat client
def connect_and_send_msg():
    ws = connect("ws://localhost:8765")
    ws.send("hello from client")
    response = ws.recv()
    print(f"response from server: {response}")

# Run the client
if __name__ == "__main__":
    connect_and_send_msg()