from enum import Enum

import json
import random

import aio_pika

from common.data_models import MessageModel, json_serial

AGENCY_EXCHANGE_NAME = "agency"
DRIVERS_EXCHANGE_NAME = "drivers"
MESSAGE_INTENSITY = 0.005  # param to set drivers random message frequency


class State(Enum):
    OFF = 0
    WORKING = 1
    REST = 2
    LAUNCH = 3


class Driver:

    def __init__(self, driver_model, connection):
        self.driver_id = driver_model.id
        self.driver_model = driver_model
        self.connection = connection
        self.connected = False
        self.active = False
        self.current_consumer_tag = None
        self.input_channel = None
        self.output_channel = None
        self.output_exchange = None
        self.state = State.OFF
        self.input_exchange = None
        self.input_queue = None
        self.message_box = []
        self.input_queue_name = "driver_in_{}".format(self.driver_id)

    async def setup(self):
        self.input_channel = await self.connection.channel()
        self.input_exchange = await self.input_channel.declare_exchange(
            DRIVERS_EXCHANGE_NAME)
        self.input_queue = await self.input_channel.declare_queue(self.input_queue_name)
        await self.input_queue.bind(exchange=DRIVERS_EXCHANGE_NAME)
        self.connected = True
        self.output_channel = await self.connection.channel()
        self.output_exchange = await self.output_channel.declare_exchange(AGENCY_EXCHANGE_NAME)
        self.current_consumer_tag = await self.input_queue.consume(self.on_message)

    async def activate(self):
        if self.connected:
            self.active = True
            print("{}: I was activated".format(self.driver_id))
            for delayed_message in self.message_box:
                # изначально я планировал отклюаться от очереди во время отключения водителя
                # однако в aio_pika столкнулся с непонятным мне поведением - после cancel не получалось продолжить consume,
                # в целях экономии времени перешел на модель промежуточной корзины сообщений
                await self.handle_message(delayed_message)
                self.message_box.remove(delayed_message)

    async def stop(self):
        if self.active:
            self.active = False
            print("{}: I was deactivated".format(self.driver_id))

    async def on_message(self, queue_message):
        agency_message = MessageModel.build_from_dict(json.loads(queue_message.body.decode('utf-8')))
        print("I've got a message: {}".format(agency_message))
        queue_message.ack()
        if self.active:
            await self.handle_message(agency_message)
        else:
            print("put in message box {}".format(agency_message))
            self.message_box.append(agency_message)

    async def handle_message(self, agency_message):
        # here can be place to handle recieved from chief
        await self.send_received(agency_message.message_id)
        await self.send_message(
            MessageModel(body=DriverMessages.got_it(), from_id=self.driver_id, to_id=agency_message.from_id))

    async def send_received(self, received_message_id):
        print("{}: sending received id: {}".format(self.driver_id, received_message_id))
        await self.output_exchange.publish(
            routing_key="agency",
            message=aio_pika.message.Message(
                json.dumps({'received_id': received_message_id}).encode('utf-8')))

    async def send_message(self, message_model):
        print("{}: sending message: {}".format(self.driver_id, message_model.to_dict()))
        await self.output_exchange.publish(
            routing_key="agency",
            message=aio_pika.message.Message(json.dumps(message_model.to_dict(), default=json_serial).encode('utf-8')))

    async def check(self, time):
        current_time = time
        # print("{}: Checking - and my time is {}, my state is {}".format(self.driver_id, current_time, self.state.name))
        if self.driver_model.working_day_start <= current_time < self.driver_model.working_day_finish:
            if self.driver_model.working_day_start <= current_time < self.driver_model.first_rest_start:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        MessageModel(from_id=self.driver_id, body=DriverMessages.hi(self.driver_model.first_rest_start),
                                     to_id=1))
                    self.state = State.WORKING

            if self.driver_model.first_rest_start <= current_time < self.driver_model.first_rest_stop:
                if self.state != State.REST:
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.rest(self.driver_model.first_rest_stop),
                                     to_id=1))
                    self.state = State.REST
                    await self.stop()

            if self.driver_model.first_rest_stop < current_time < self.driver_model.launch_rest_start:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.back_to_work(self.driver_model.launch_rest_start),
                                     to_id=1))
                    self.state = State.WORKING

            if self.driver_model.launch_rest_start <= current_time < self.driver_model.launch_rest_stop:
                if self.state != State.LAUNCH:
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.launch(self.driver_model.launch_rest_stop),
                                     to_id=1))
                    self.state = State.LAUNCH
                    await self.stop()

            if self.driver_model.launch_rest_stop < current_time < self.driver_model.second_rest_start:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.back_to_work(self.driver_model.second_rest_start),
                                     to_id=1))
                    self.state = State.WORKING

            if self.driver_model.second_rest_start <= current_time < self.driver_model.second_rest_stop:
                if self.state != State.REST:
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.rest(self.driver_model.second_rest_stop),
                                     to_id=1))
                    self.state = State.REST
                    await self.stop()

            if self.driver_model.second_rest_stop < current_time < self.driver_model.third_rest_start:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.back_to_work(self.driver_model.third_rest_start),
                                     to_id=1))
                    self.state = State.WORKING

            if self.driver_model.third_rest_start <= current_time < self.driver_model.third_rest_stop:
                if self.state != State.REST:
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.rest(self.driver_model.third_rest_stop),
                                     to_id=1))
                    self.state = State.REST
                    await self.stop()

            if self.driver_model.third_rest_stop <= current_time < self.driver_model.working_day_finish:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        MessageModel(from_id=self.driver_id,
                                     body=DriverMessages.back_to_work(self.driver_model.working_day_finish),
                                     to_id=1))
                    self.state = State.WORKING

        else:
            if self.state != State.OFF:
                await self.send_message(
                    MessageModel(from_id=self.driver_id,
                                 body=DriverMessages.stop(self.driver_model.working_day_start),
                                 to_id=1))
                self.state = State.OFF
                await self.stop()

        if self.state == State.WORKING:
            if random.random() < MESSAGE_INTENSITY:
                await self.send_message(
                    MessageModel(from_id=self.driver_id,
                                 body=DriverMessages.simple_message(),
                                 to_id=1))


class DriverMessages:  # todo think about enum

    @staticmethod
    def hi(until_time):
        return "Hi, I'm online until {}".format(until_time)

    @staticmethod
    def rest(until_time):
        return "I'm on rest until {}".format(until_time)

    @staticmethod
    def launch(until_time):
        return "I'm on launch until {}".format(until_time)

    @staticmethod
    def back_to_work(until_time):
        return "I'm working and online. Until {}".format(until_time)

    @staticmethod
    def got_it():
        return "Got it"

    @staticmethod
    def confused():
        return "I'm confused by your last message. Please explain more detailed"

    @staticmethod
    def stop(until_time):
        return "I'm done for today. I will be offline until {}".format(until_time)

    @staticmethod
    def simple_message():
        return "It's simple message for you when I'm working"
