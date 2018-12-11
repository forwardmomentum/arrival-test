# -*-  coding: utf-8 -*-
import datetime
import logging
import pika
import json

from aio_pika import connect_robust
import aio_pika

import db_controller
from common.data_models import json_serial
from db_controller import MessageModel

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
        message_model = MessageModel(body=message_dict["body"], to_id=message_dict["to_id"], from_id=1,
                                     sended_at=datetime.datetime.now())
        routing_key = 'driver_in_{}'.format(message_model.to_id)
        engine = await db_controller.get_engine()
        async with engine.acquire() as conn:
            await db_controller.add_message(conn, message_model)
            print("Sending message to {} : {}".format(message_model.to_id, message_model.to_dict()))
            await self.to_drivers_exchange.publish(
                routing_key=routing_key,
                message=aio_pika.message.Message(
                    json.dumps(message_model.to_dict(), default=json_serial).encode("utf-8")))
        for sess_id in self.websockets:
            self.websockets[sess_id].write_message(
                json.dumps(message_model.to_dict(),
                           default=json_serial))

    async def on_message(self, queue_message):
        message_dict = json.loads(queue_message.body.decode('utf-8'))
        engine = await db_controller.get_engine()
        if 'received_id' in message_dict:
            print("Received {}".format(message_dict))
            async with engine.acquire() as conn:
                await db_controller.message_received(conn, message_dict['received_id'])
            # if queue_message.routing_key in self.websockets:
            #     self.websockets[queue_message.routing_key].write_message(json.dumps(message_dict))
            for sess_id in self.websockets:
                self.websockets[sess_id].write_message(json.dumps(message_dict))
            queue_message.ack()
            return
        message_model = MessageModel.build_from_dict(message_dict)
        message_model.received = True
        print("Got message from {}: {}".format(message_model.from_id, message_model.to_dict()))
        async with engine.acquire() as conn:
            await db_controller.add_message(conn, message_model)
        # if queue_message.routing_key in self.websockets:  # routing key can be used in multi chief model
        #     self.websockets[queue_message.routing_key].write_message(
        #         json.dumps(message_model.to_dict(),
        #                    default=json_serial))
        for sess_id in self.websockets:
            self.websockets[sess_id].write_message(
                json.dumps(message_model.to_dict(),
                           default=json_serial))
        queue_message.ack()
