# -*-  coding: utf-8 -*-
import logging
import pika
import json

from aio_pika import connect_robust
import aio_pika
from pika.adapters import TornadoConnection

from driver import Message

pika.log = logging.getLogger(__name__)

AGENCY_QUEUE_NAME = 'agency_queue'
AGENCY_CHANNEL_NAME = 'agency'
AGENCY_EXCHANGE_NAME = 'agency'
AGENCY_ROUTING_KEY = 'agency'
DRIVERS_EXCHANGE_NAME = 'drivers'
RABBITMQ_USERNAME = 'rabbitmq'
RABBITMQ_PASSWORD = 'rabbitmq'
RABBITMQ_HOST = 'localhost'


class MessageService(object):

    def __init__(self):
        self.connected = False
        self.connecting = False
        self.connection = None
        self.to_drivers_channel = None
        self.to_drivers_exchange = None
        self.out_channels = {}
        self.websockets = {}

    async def connect(self):
        if self.connecting:
            return
        self.connecting = True

        self.connection = await connect_robust(login=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
        self.connected = True

        self.to_drivers_channel = await self.connection.channel()
        self.to_drivers_exchange = await self.to_drivers_channel.declare_exchange(DRIVERS_EXCHANGE_NAME)

        output_channel = await self.connection.channel()

        await output_channel.declare_exchange(name='agency')
        self.out_channels[AGENCY_CHANNEL_NAME] = output_channel
        queue = await output_channel.declare_queue(
            name=AGENCY_QUEUE_NAME)
        await queue.bind(exchange=AGENCY_EXCHANGE_NAME,
                         routing_key=AGENCY_ROUTING_KEY)
        await queue.consume(self.on_message)

    def register_websocket(self, sess_id, ws):
        self.websockets[sess_id] = ws

    def unregister_websocket(self, sess_id):
        del self.websockets[sess_id]
        print('unregistered ws connection with id: {}'.format(sess_id))

    async def handle_message(self, raw_message):
        message_dict = json.loads(raw_message)
        message_body, driver_id = message_dict["message_body"], message_dict["driver_id"]
        routing_key = 'driver_in_{}'.format(driver_id)
        # todo save message in db, take id of message
        message_to_send = Message(type='message', message_body=message_body,
                                  message_id='TODO GET ID FROM POSTGRES',
                                  from_id='agency')
        print("Sending message to {} : {}".format(driver_id, message_to_send))
        await self.to_drivers_exchange.publish(
            routing_key=routing_key,
            message=aio_pika.message.Message(message_to_send.to_json().encode("utf-8")))

    def on_message(self, queue_message):
        message = Message.build_from_json(queue_message.body)
        print("Got message from {}: {}".format(message.from_id, message))
        # todo записать в базу если сообщение, изменить статус сообщения если recieved
        if queue_message.routing_key in self.websockets:  # routing key can be used in multi chief model
            self.websockets[queue_message.routing_key].write_message(
                message.to_json())  # проброс нотификаций по всему подряд
        queue_message.ack()
