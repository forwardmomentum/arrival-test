#!/usr/bin/env python
"""
App to emulate behaviour of multiple drivers
"""
import asyncio
import json
import datetime

import tornado
from aio_pika import connect_robust
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import PeriodicCallback

from common.data_models import UserModel
from driver import Driver

RABBITMQ_USERNAME = 'rabbitmq'
RABBITMQ_PASSWORD = 'rabbitmq'
DRIVERS_DATA_URL = "http://localhost:9001/api/drivers"


class Scheduler(object):
    """
    Scheduler controls each driver lifecycle (init, wake, rest)
    """

    def __init__(self):
        self.drivers = {}
        self.connected = False
        self.connection = None
        self.out_channels = None
        self.all_drivers_data = []
        self.time = datetime.time(11, 30)

    async def connect(self):
        self.connection = await connect_robust(login=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
        self.connected = True
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(DRIVERS_DATA_URL)
        self.all_drivers_data = [UserModel.build_from_dict(user) for user in json.loads(response.body)]
        print("Drivers data fetched from agency")
        http_client.close()
        await self.init_drivers()

    async def init_drivers(self):
        for driver_model in self.all_drivers_data:
            try:
                if driver_model.id not in self.drivers:
                    self.drivers[driver_model.id] = Driver(driver_model, self.connection)
                    await self.drivers[driver_model.id].setup()
            except ValueError:
                print("Can not create driver with model: {}".format(driver_model.to_dict()))

    async def check_drivers(self):
        """
        Scheduled method to check all drivers and send them signals to wake, sleep etc
        :return:
        """
        if self.connected:
            # self.time = (datetime.datetime.combine(datetime.date(1, 1, 1), self.time) + datetime.timedelta(
            #     minutes=5)).time()
            self.time = datetime.datetime.now().time()
            for driver_id in self.drivers:
                await self.drivers[driver_id].check(self.time)
        else:
            print("Waiting for connection to check drivers")


if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)
    scheduler = Scheduler()
    io_loop.asyncio_loop.run_until_complete(scheduler.connect())
    scheduled_task = PeriodicCallback(scheduler.check_drivers, 2000)
    scheduled_task.start()
    io_loop.start()
