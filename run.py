# coding: utf-8
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.web import RequestHandler, Application, url
from messages.callbacks import save_messages
from messages.handlers import MessageUpdatesHandler, MessageNewHandler
from users.handlers import UserHandler
from settings import *


class HelloHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        # print('Home')
        self.write("Hello, world")


def make_app():
    return Application([
        url(r'/', HelloHandler),
        url(r'/users/', UserHandler),
        url(r'/messages/', MessageUpdatesHandler),
        url(r'/messages/create/', MessageNewHandler)
    ])


def main():
    parse_command_line()
    app = make_app()
    app.listen(8888)
    IOLoop.instance().add_callback(save_messages)
    IOLoop.current().start()

if __name__ == '__main__':
    main()