#!/usr/bin/env python
import pika
import sys
import config
print("run queue client")
cfg = config.get_env_config()
print("get connection")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=cfg.queue.host, port=cfg.queue.port))
channel = connection.channel()
print("got channel")
channel.queue_declare(queue=cfg.queue.queue_name, durable=cfg.queue.durable)
print("defined queue")
message = ' '.join(sys.argv[1:]) or "standard message"
print("about to send message" + message)
channel.basic_publish(
    exchange='',
    routing_key=cfg.queue.queue_name,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))
print("sent backend message: " + message)
connection.close()