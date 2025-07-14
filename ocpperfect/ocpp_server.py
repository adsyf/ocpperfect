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
import config
import time
cfg = config.get_env_config()
connected_clients = set()

class OCPPServer(object):
    def __init__(self):
        self.server = None

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
        connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.queue.host))
        channel = connection.channel()

        channel.queue_declare(queue=cfg.queue.queue_name, durable=cfg.queue.durable)
        channel.basic_consume(queue=cfg.queue.queue_name, on_message_callback=self.queue_callback, auto_ack=cfg.queue.auto_ack)

        print('start consuming from queue')
        channel.start_consuming()

    async def start_websocket_server(self):
        print("Starting websocket")
        self.server = await websockets.serve(self.handle_websocket_client, cfg.websocket.host, cfg.websocket.port)
        print("awaiting websocket server")
        await self.server.wait_closed()
        print("websocket server closed")

    def non_async_start_websocket_server(self):
        asyncio.run(self.start_websocket_server())

    def start_ocpp_server(self):
        print("about to define queue thread")
        queue_thread = threading.Thread(target=self.consume_queue)
        print("queue_thread defined")
        queue_thread.start()
        print("queue_thread started")
        #websocket_thread = threading.Thread(target=self.non_async_start_websocket_server)
        websocket_thread = threading.Thread(target=asyncio.run,args=[self.start_websocket_server()],daemon=True)

        print("websocket_thread defined")
        websocket_thread.start()
        #websocket_thread.join()
        print("websocket_thread started")
        #self.non_async_start_websocket_server()

    def stop_ocpp_server(self):
        print("try stop ocpp_server")
        var = self.server.stop()
        print("stopped ocpp_server")


if __name__ == "__main__":
    print("define ocpp server")
    ocpp_server = OCPPServer()
    print("try start ocpp server")
    ocpp_server.start_ocpp_server()
    print("ocpp server started")
    print("try sleep 5")
    time.sleep(5)
    print("slept 5")
    #print("try stop ocpp server")
    #ocpp_server.stop_ocpp_server()
    #print("ocpp server stopped")
