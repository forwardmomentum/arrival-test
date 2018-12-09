from enum import Enum

import datetime
import json
import random

import aio_pika

AGENCY_EXCHANGE_NAME = "agency"
DRIVERS_EXCHANGE_NAME = "drivers"
MESSAGE_INTENSITY = 0.05  # param to manage drivers random message frequency


class State(Enum):
    OFF = 0
    WORKING = 1
    REST = 2
    LAUNCH = 3


class Message:

    def __init__(self, type, message_body, from_id, message_id=None):
        self.type = type
        self.message_id = message_id
        self.message_body = message_body
        self.from_id = from_id

    @staticmethod
    def build_from_json(json_message):
        message_dict = json.loads(json_message)
        return Message(message_dict["type"], message_dict["message_body"], message_dict["from_id"],
                       message_dict["message_id"])

    def to_json(self):
        return json.dumps({
            'type': self.type,
            'message_id': self.message_id,
            'message_body': self.message_body,
            'from_id': self.from_id
        })

    def __str__(self):
        return self.to_json()


class Driver:

    def __init__(self, driver_data, connection):
        self.driver_id = driver_data["driver_id"]
        self.driver_data = driver_data
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
        self.time = datetime.time(11, 30)  # fixme: only for testing purposes!
        self.input_queue_name = "driver_in_{}".format(self.driver_id)

    async def setup(self):
        self.input_channel = await self.connection.channel()
        self.input_exchange = await self.input_channel.declare_exchange(
            DRIVERS_EXCHANGE_NAME)  # todo can be moved into scheduler?
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
        agency_message = Message.build_from_json(queue_message.body)
        print("I've got a message: {}".format(agency_message))
        queue_message.ack()
        if self.active:
            await self.handle_message(agency_message)
        else:
            print("put in message box {}".format(agency_message))
            self.message_box.append(agency_message)

    async def handle_message(self, agency_message):
        if agency_message.type == 'received':
            return
        await self.send_received(agency_message.message_id)
        await self.send_message(Message(type='message', message_body=DriverMessages.got_it(), from_id=self.driver_id
                                        ))

    async def send_received(self, received_message_id):
        print("{}: I want to send received to message with id: {}".format(self.driver_id, received_message_id))
        await self.output_exchange.publish(
            routing_key="agency",
            message=aio_pika.message.Message(
                Message(type='received', message_body=received_message_id,
                        from_id=self.driver_id).to_json().encode('utf-8')))

    async def send_message(self, message):
        print("{}: I want to send message: {}".format(self.driver_id, message))
        await self.output_exchange.publish(
            routing_key="agency",
            message=aio_pika.message.Message(message.to_json().encode('utf-8')))

    async def check(self):
        self.time = (
                datetime.datetime.combine(datetime.date(1, 1, 1), self.time) + datetime.timedelta(minutes=5)).time()
        current_time = self.time
        print("{}: Checking - and my time is {}, my state is {}".format(self.driver_id, current_time, self.state.name))
        schedule = self.driver_data["schedule"]
        # todo check week day
        if schedule['working_day_start'] <= current_time < schedule['working_day_finish']:
            if schedule['working_day_start'] <= current_time < schedule['first_rest_start']:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.hi(schedule['first_rest_start']),
                                from_id=self.driver_id))
                    self.state = State.WORKING

            if schedule['first_rest_start'] <= current_time < schedule['first_rest_stop']:
                if self.state != State.REST:
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.rest(schedule['first_rest_stop']),
                                from_id=self.driver_id))
                    self.state = State.REST
                    await self.stop()

            if schedule['first_rest_stop'] < current_time < schedule['launch_rest_start']:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.back_to_work(schedule['launch_rest_start']),
                                from_id=self.driver_id))
                    self.state = State.WORKING

            if schedule['launch_rest_start'] <= current_time < schedule['launch_rest_stop']:
                if self.state != State.LAUNCH:
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.launch(schedule['launch_rest_stop']),
                                from_id=self.driver_id))
                    self.state = State.LAUNCH
                    await self.stop()

            if schedule['launch_rest_stop'] < current_time < schedule['second_rest_start']:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.back_to_work(schedule['second_rest_start']),
                                from_id=self.driver_id))
                    self.state = State.WORKING

            if schedule['second_rest_start'] <= current_time < schedule['second_rest_stop']:
                if self.state != State.REST:
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.rest(schedule['second_rest_stop']),
                                from_id=self.driver_id))
                    self.state = State.REST
                    await self.stop()

            if schedule['second_rest_stop'] < current_time < schedule['third_rest_start']:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.back_to_work(schedule['third_rest_start']),
                                from_id=self.driver_id))
                    self.state = State.WORKING

            if schedule['third_rest_start'] <= current_time < schedule['third_rest_stop']:
                if self.state != State.REST:
                    await self.send_message(
                        Message(type='message', message_body=DriverMessages.rest(schedule['third_rest_stop']),
                                from_id=self.driver_id))
                    self.state = State.REST
                    await self.stop()

            if schedule['third_rest_stop'] <= current_time < schedule['working_day_finish']:
                if self.state != State.WORKING:
                    await self.activate()
                    await self.send_message(
                        Message(type='message',
                                message_body=DriverMessages.back_to_work(schedule['working_day_finish']),
                                from_id=self.driver_id))
                    self.state = State.WORKING

        else:
            if self.state != State.OFF:
                await self.send_message(
                    Message(type='message',
                            message_body=DriverMessages.stop(schedule['working_day_start']),
                            from_id=self.driver_id))
                self.state = State.OFF
                await self.stop()

        if self.state == State.WORKING:
            if random.random() < MESSAGE_INTENSITY:
                await self.send_message(
                    Message(type='message',
                            message_body=DriverMessages.simple_message(),
                            from_id=self.driver_id))


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
