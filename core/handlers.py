# coding: utf-8
from __future__ import unicode_literals
from tornado.options import options
from tornado.web import RequestHandler
from users.buffer import global_user_buffer


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        if options.debug:
            self.set_header("Access-Control-Allow-Origin", "*")
            return
        self.set_header("Access-Control-Allow-Origin", ", ".join(options.allowed_hosts))


class ServerBaseHandler(BaseHandler):

    def prepare(self):
        if self.request.remote_ip not in options.allowed_hosts and not options.debug:
            self.clear()
            self.set_status(403)
            self.finish({'error': 'IP not allowed'})


class UserBaseHandler(BaseHandler):

    def prepare(self):
        token = self.get_argument('token', None)
        if token is None:
            self.set_status(400)
            self.finish({'error': 'no token'})
            return
        self.user = global_user_buffer.get_user(token)