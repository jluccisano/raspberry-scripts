#!/usr/bin/python
import pika
import time
import datetime
import json
import logging
import argparse
from scripts.dht22 import dht22
import os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class Publisher:

    def __init__(self, url, gatewayId, sendFrom, exchange, publish_interval):

        self._url = url
        self._stopping = False
        self._connection = None
        self._channel = None
        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self.EXCHANGE = exchange
        self.EXCHANGE_TYPE = "headers"
        self.PUBLISH_INTERVAL = publish_interval
        self.GATEWAY_ID = gatewayId
        self.SENDFROM = sendFrom
        self.ROUTING_KEY = ''


    def connect(self):
        if not self._connection or self._connection.is_closed:
            LOGGER.info('Connecting to %s', self._url)
            self._connection = pika.BlockingConnection(pika.URLParameters(self._url))
            return pika.SelectConnection(pika.URLParameters(self._url),
                                         on_open_callback=self.on_connection_open,
                                         on_close_callback=self.on_connection_closed,
                                         stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self._connection.ioloop.stop)

    def open_channel(self):
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)


    def on_channel_closed(self, channel, reply_code, reply_text):
        LOGGER.warning('Channel was closed: (%s) %s', reply_code, reply_text)
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        LOGGER.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(callback=self.on_exchange_declareok, exchange= self.EXCHANGE, type=self.EXCHANGE_TYPE, durable=True)


    def on_exchange_declareok(self, param):
        LOGGER.info('Exchange declared')
        self.start_publishing()

    def start_publishing(self):
        LOGGER.info('Start publishing')
        #self.enable_delivery_confirmations()
        self.schedule_next_message()

    def enable_delivery_confirmations(self):
        LOGGER.info('Enable Confirm.Select RPC command')
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('Received %s for delivery tag: %i',
                    confirmation_type,
                    method_frame.method.delivery_tag)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)
        LOGGER.info('Published %i messages, %i have yet to be confirmed, '
                    '%i were acked and %i were nacked',
                    self._message_number, len(self._deliveries),
                    self._acked, self._nacked)


    def schedule_next_message(self):
        LOGGER.info('Scheduling next message for %0.1f seconds',
                    self.PUBLISH_INTERVAL)
        self._connection.add_timeout(self.PUBLISH_INTERVAL,
                                     self.publish)

    def publish(self):

        if self._channel is None or not self._channel.is_open:
            return


        timestamp = time.time()
        now = datetime.datetime.now()
        expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())

        headers = {
            'sendFrom': self.SENDFROM,
            'gatewayId': self.GATEWAY_ID,
            'content_type': 'application/json',
            'created': int(timestamp)
        }

        data = {
            'data': dht22.getData_func(),
            'created': int(timestamp),
            'expire': expire
        }

        self._channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=1,
                type='DHT22',
                content_type='application/json',
                priority=0,
                timestamp=int(timestamp),
                expiration=str(expire),
                headers=headers
            ))

        self._message_number += 1
        self._deliveries.append(self._message_number)
        LOGGER.info('[>] Published data %r # %i', data, self._message_number)
        self.schedule_next_message()


    def run(self):

        while not self._stopping:
            self._connection = None
            self._deliveries = []
            self._acked = 0
            self._nacked = 0
            self._message_number = 0

            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop()
                if (self._connection is not None and
                        not self._connection.is_closed):
                    # Finish closing
                    self._connection.ioloop.start()

        LOGGER.info('Stopped')

    def stop(self):
        LOGGER.info('Stopping')
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        if self._channel is not None:
            LOGGER.info('Closing the channel')
            self._channel.close()

    def close_connection(self):
        if self._connection is not None:
            LOGGER.info('Closing connection')
            self._connection.close()



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--amqp-url', help='URL of RabbitMQ instance', required=True)
    parser.add_argument('--gatewayId',help='Gateway ID', required=True)
    parser.add_argument('--sendFrom', help='Send from', required=True)
    parser.add_argument('--exchange', help='Exchange name', required=True)
    parser.add_argument('--publish-interval', help='Interval delay to send data', type=int, required=True)
    parser.add_argument('--log-path', help='Path of log', required=True)

    args = parser.parse_args()

    if not os.path.isdir(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))

    logging.basicConfig(filename=args.log_path+"/publisher.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

    publisher = Publisher(args.amqp_url+'/%2F?connection_attempts=10&heartbeat_interval=3600', args.gatewayId, args.sendFrom, args.exchange, args.publish_interval)
    publisher.run()


if __name__ == '__main__':
    main()