# -*-  coding: utf-8 -*-
"""
Agency server (tornado web service) provides REST and WS interfaces for chief,
 handles messages from chief and drivers (via RabbitMQ), works with PostgreSQL storage
"""
import asyncio

import tornado

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

    @web.asynchronous
    def get(self, *args):
        self.render('connector.html')


class Index(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.render('index.html')


app = web.Application([
    (r'/ws', SocketHandler),
    (r'/connect', Connect),
    (r'/', Index),
])


def runserver():
    tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    io_loop = tornado.ioloop.IOLoop.current()
    asyncio.set_event_loop(io_loop.asyncio_loop)

    app.message_service = MessageService()

    io_loop.asyncio_loop.run_until_complete(app.message_service.connect())

    app.listen(9001)
    io_loop.start()


if __name__ == '__main__':
    runserver()
