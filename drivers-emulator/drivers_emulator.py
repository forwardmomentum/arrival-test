#!/usr/bin/env python
"""
App to emulate behaviour of multiple drivers
"""
import asyncio

import pika
import datetime
import logging

import tornado
from aio_pika import connect_robust
from pika import TornadoConnection
from tornado import ioloop
from tornado.ioloop import PeriodicCallback

from driver import Driver

# TODO read from agency service (one by one?)
from message_service import RABBITMQ_USERNAME, RABBITMQ_PASSWORD

all_drivers_data = [
    {
        "driver_id": "111qqq",
        "name": "Jack Johnson Hopkins",
        "email": "jack@gmail.com",
        "birthday": datetime.date(1990, 3, 5),
        "phone": "+79229223344",
        "schedule": {
            "working_day_start": datetime.time(8, 0),
            "working_day_finish": datetime.time(20, 0),
            "first_rest_start": datetime.time(10,0),
            "first_rest_stop": datetime.time(10, 20),
            "launch_rest_start": datetime.time(12, 0),
            "launch_rest_stop": datetime.time(13, 0),
            "second_rest_start": datetime.time(15, 0),
            "second_rest_stop": datetime.time(15, 20),
            "third_rest_start": datetime.time(18, 0),
            "third_rest_stop": datetime.time(18, 20),
            "working_week_days": [0, 1, 2, 3, 4]
        }
    },
    {
        "driver_id": "222www",
        "name": "Homer Peter Griffin",
        "email": "",
        "birthday": datetime.date(1980, 3, 6),
        "phone": "+79054443322",
        "schedule": {
            "working_day_start": datetime.time(7, 0),
            "working_day_finish": datetime.time(19, 0),
            "first_rest_start": datetime.time(9,0),
            "first_rest_stop": datetime.time(9, 20),
            "launch_rest_start": datetime.time(11, 30),
            "launch_rest_stop": datetime.time(12, 30),
            "second_rest_start": datetime.time(14, 0),
            "second_rest_stop": datetime.time(14, 20),
            "third_rest_start": datetime.time(17, 0),
            "third_rest_stop": datetime.time(17, 20),
            "working_week_days": [1, 2, 3, 4, 5]
        }
    },
    {
        "driver_id": "333eee",
        "name": "Gene Peter Simmons",
        "email": "gene@gmail.com",
        "birthday": datetime.date(1985, 3, 8),
        "phone": "+79054443325",
        "schedule": {
            "working_day_start": datetime.time(9, 0),
            "working_day_finish": datetime.time(20, 0),
            "first_rest_start": datetime.time(10,0),
            "first_rest_stop": datetime.time(10, 20),
            "launch_rest_start": datetime.time(12, 0),
            "launch_rest_stop": datetime.time(13, 0),
            "second_rest_start": datetime.time(15, 0),
            "second_rest_stop": datetime.time(15, 20),
            "third_rest_start": datetime.time(18, 0),
            "third_rest_stop": datetime.time(18, 20),
            "working_week_days": [2, 3, 4, 5, 6]
        }
    }
]


class Scheduler(object):
    """
    Scheduler controls each driver lifecycle (init, wake, rest)
    """

    def __init__(self):
        self.drivers = {}
        self.connected = False
        self.connection = None
        self.out_channels = None

    async def connect(self):
        self.connection = await connect_robust(login=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
        self.connected = True
        # todo fetch drivers data
        await self.init_drivers()

    def on_connected(self, connection):
        self.connected = True
        self.connection = connection
        # todo fetch drivers data
        self.init_drivers()

    async def init_drivers(self):
        for driver_data in all_drivers_data[:1]:
            try:
                if driver_data["driver_id"] not in self.drivers:
                    self.drivers[driver_data["driver_id"]] = Driver(driver_data, self.connection)
                    await self.drivers[driver_data["driver_id"]].setup()
            except ValueError:
                print("Can not create driver with data: {}".format(driver_data))

    async def check_drivers(self):
        """
        Scheduled method to check all drivers and send them signals to wake, sleep etc
        :return:
        """
        if self.connected:
            for driver_id in self.drivers:
                await self.drivers[driver_id].check()
        else:
            print("Waiting for connection to check drivers")


if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)
    scheduler = Scheduler()
    io_loop.asyncio_loop.run_until_complete(scheduler.connect())
    scheduled_task = PeriodicCallback(scheduler.check_drivers, 1000)
    scheduled_task.start()
    io_loop.start()

