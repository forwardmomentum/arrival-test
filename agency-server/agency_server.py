# -*-  coding: utf-8 -*-
"""
Agency server (tornado web service) provides REST and WS interfaces for chief,
 handles messages from chief and drivers (via RabbitMQ), works with PostgreSQL storage
"""
import asyncio
import sys
import tornado
import json

import db_controller
from db_controller import prepare_db
from message_service import MessageService

from tornado import websocket, web, ioloop


class IndexHandler(web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class SocketHandler(websocket.WebSocketHandler):

    def data_received(self, chunk):
        pass

    def check_origin(self, origin):
        return True

    def _get_sess_id(self):
        return self.sess_id

    def open(self):
        self.sess_id = 'agency'  # for multi users case can be linked with username
        self.application.message_service.register_websocket(self._get_sess_id(), self)

    async def on_message(self, message):
        await self.application.message_service.handle_message(message)

    def on_close(self):
        self.application.message_service.unregister_websocket(self._get_sess_id())


class Connect(web.RequestHandler):

    async def get(self, *args):
        self.render('connector.html')


class Index(web.RequestHandler):

    async def get(self, *args):
        self.render('index.html')


class HistoryHandler(web.RequestHandler):

    async def get(self, driver_id):
        """
        Get json with whole messages between chief and driver with driver_id
        """
        engine = await db_controller.get_engine()
        async with engine.acquire() as conn:
            result = await db_controller.read_messages_history(conn, driver_id)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, default=db_controller.json_serial))


class DriverHandler(web.RequestHandler):

    async def get(self, driver_id):
        """
        Get json with drivers data and short message history
        """
        engine = await db_controller.get_engine()
        async with engine.acquire() as conn:
            result = await db_controller.read_driver_with_short_history(conn, driver_id)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, default=db_controller.json_serial))


class AllDriversHandler(web.RequestHandler):

    async def get(self):
        """
        Get json list with all drivers data
        """
        engine = await db_controller.get_engine()
        async with engine.acquire() as conn:
            result = await db_controller.read_all_drivers(conn)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, default=db_controller.json_serial))


class MessageHandler(web.RequestHandler):

    async def get(self):
        """
        Get last 100 messages
        """
        engine = await db_controller.get_engine()
        async with engine.acquire() as conn:
            result = await db_controller.read_last_messages(conn)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, default=db_controller.json_serial))


app = web.Application([
    (r'/ws', SocketHandler),
    (r'/connect', Connect),
    (r'/', Index),
    (r'/api/drivers/([^/]+)/history', HistoryHandler),
    (r'/api/drivers/([^/]+)', DriverHandler),
    (r'/api/drivers', AllDriversHandler),
    (r'/api/messages', MessageHandler)
])


async def setup_db(drivers_count):
    engine = await db_controller.get_engine()
    async with engine.acquire() as conn:
        await prepare_db(conn, drivers_count)


def runserver(drivers_count=None):
    tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)
    if drivers_count:
        io_loop.asyncio_loop.run_until_complete(setup_db(drivers_count))
    app.message_service = MessageService()
    io_loop.asyncio_loop.run_until_complete(app.message_service.connect())
    app.listen(9001)
    io_loop.start()


if __name__ == '__main__':
    if sys.argv[1]:
        runserver(int(sys.argv[1]))
    else:
        runserver()
