#!/usr/bin/env python
import asyncio
import pika
import threading
import websockets
#https://codemia.io/knowledge-hub/path/consuming_rabbitmq_queue_from_inside_python_threads
#https://websockets.readthedocs.io/en/stable/intro/examples.html
#https://medium.com/@AlexanderObregon/building-real-time-applications-with-python-and-websockets-eb33a4098e02
import config
cfg = config.get_env_config()
connected_clients = set()
async def handle_websocket_client(websocket):
    print("handle client")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("received message from websocket client " + message)
            await websocket.send("got your message buddy i.e. " + message)
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

def queue_callback(ch, method, properties, body):
    print(f"received message from queue {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.queue.host))
    channel = connection.channel()

    channel.queue_declare(queue=cfg.queue.queue_name, durable=cfg.queue.durable)
    channel.basic_consume(queue=cfg.queue.queue_name, on_message_callback=queue_callback, auto_ack=cfg.queue.auto_ack)

    print('start consuming from queue')
    channel.start_consuming()

async def start_websocket():
    print("Starting websocket")
    server = await websockets.serve(handle_websocket_client, cfg.websocket.host, cfg.websocket.port)
    print("awaiting websocket server")
    await server.wait_closed()
    print("websocket server closed")

def main():
    print("about to define thread")
    thread = threading.Thread(target=consume_queue)
    print("thread defined")
    thread.start()
    print("after thread started")
    asyncio.run(start_websocket())

if __name__ == "__main__":
    main()