#!/usr/bin/env python
import asyncio
import pika
import threading
import websockets
#https://codemia.io/knowledge-hub/path/consuming_rabbitmq_queue_from_inside_python_threads
#https://websockets.readthedocs.io/en/stable/intro/examples.html
#https://medium.com/@AlexanderObregon/building-real-time-applications-with-python-and-websockets-eb33a4098e02
#https://www.frederikbanke.com/integration-testing-in-python-rabbitmq/
#https://stackoverflow.com/questions/31901356/python-unittest-websocket-server
#https://docs.python.org/3/library/asyncio.html
from config import *
import time
connected_clients = set()

def debug_imports():
    import sys
    import os
    print("Python version:", sys.version)
    print("\nPython executable:", sys.executable)
    print("\nPYTHONPATH:")
    for path in sys.path:
        print(f"  - {path}")

    print("\nCurrent working directory:", os.getcwd())
    print("\nInstalled packages:")
    import pkg_resources
    installed_packages = [f"{dist.key} ({dist.version})"
                         for dist in pkg_resources.working_set]
    for package in sorted(installed_packages):
        print(f"  - {package}")


class OCPPServer(object):
    def __init__(self):
        self.server = None
        self.queue_thread = None
        self.websocket_thread = None
        self.cfg = get_env_config()
        print(self.cfg)

    async def handle_websocket_client(self,websocket):
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

    def queue_callback(self,ch, method, properties, body):
        print(f"received message from queue {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_queue(self,):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.cfg.queue.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.cfg.queue.queue_name, durable=self.cfg.queue.durable)
        channel.basic_consume(queue=self.cfg.queue.queue_name, on_message_callback=self.queue_callback, auto_ack=self.cfg.queue.auto_ack)

        print('start consuming from queue')
        channel.start_consuming()

    async def start_websocket_server(self):
        print("Starting websocket")
        self.server = await websockets.serve(self.handle_websocket_client, self.cfg.websocket.host, self.cfg.websocket.port)
        print("awaiting websocket server")
        await self.server.wait_closed()
        print("websocket server closed")

    def non_async_start_websocket_server(self):
        asyncio.run(self.start_websocket_server())

    def start_ocpp_server(self):
        print("about to define queue thread")
        self.queue_thread = threading.Thread(target=self.consume_queue)
        print("queue_thread defined")
        self.queue_thread.start()
        print("queue_thread started")
        #websocket_thread = threading.Thread(target=self.non_async_start_websocket_server)
        self.websocket_thread = threading.Thread(target=asyncio.run,args=[self.start_websocket_server()],daemon=True)

        print("websocket_thread defined")
        self.websocket_thread.start()
        #self.websocket_thread.join()
        print("websocket_thread started")
        #self.non_async_start_websocket_server()

    async def stop_ocpp_server(self):
        print("try stop ocpp_server")
        print("queue thread is alive: " + str(self.queue_thread.is_alive()))
        print("websocket thread is alive: " + str(self.websocket_thread.is_alive()))
        print("queue thread is daemon: " + str(self.queue_thread.daemon))
        print("websocket thread is daemon: " + str(self.websocket_thread.daemon))
        self.server.close()
        print("request server closed")

        time.sleep(2)
        await self.server.wait_closed()
        print("server wait closed")

        print("queue thread is alive: " + str(self.queue_thread.is_alive()))
        print("websocket thread is alive: " + str(self.websocket_thread.is_alive()))
        print("queue thread is daemon: " + str(self.queue_thread.daemon))
        print("websocket thread is daemon: " + str(self.websocket_thread.daemon))
        print("stopped ocpp_server")



if __name__ == "__main__":
    debug_imports()
    print("define ocpp server")
    ocpp_server = OCPPServer()
    print("try start ocpp server")
    ocpp_server.start_ocpp_server()
    print("ocpp server started")
    #print("try sleep 2")
    time.sleep(2)
    #print("slept 2")
    #print("try stop ocpp server")
    #asyncio.run(ocpp_server.stop_ocpp_server())
    #print("ocpp server stopped")
    #ocpp_server = None

