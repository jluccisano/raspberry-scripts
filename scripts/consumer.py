#!/usr/bin/python
import pika

queue = 'queue_raspberry_1'
exchange = 'events'

def on_message(channel, method_frame, header_frame, body):
    if body.startswith("queue:"):
        key = body + "_key"
        print("Declaring queue %s bound with key %s" %(queue, key))
    else:
        print("Message body", body)

connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@192.95.25.173:5672/%2F?heartbeat_interval=1'))

channel = connection.channel()
channel.exchange_declare(exchange="events", exchange_type="headers", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(queue=queue, exchange=exchange, routing_key="", arguments={ 'gatewayId': 'raspberry_1', 'x-match': 'any'})

channel.basic_qos(prefetch_count=1)

channel.basic_consume(on_message, queue,no_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
