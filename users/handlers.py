# coding: utf-8
from __future__ import unicode_literals
from tornado.escape import json_decode
from tornado.options import options
from tornado.web import HTTPError
from core.handlers import ServerBaseHandler
from users.buffer import global_user_buffer


class UserHandler(ServerBaseHandler):

    def get(self, *args, **kwargs):
        if options.debug:
            token = global_user_buffer.add_user({
                'id': 1,
                'first_name': 'Teste',
                'last_name': 'user',
                'nickname': 'teste'
            })
            self.write({'token': token})
        else:
            raise HTTPError(405)

    def post(self, *args, **kwargs):
        data = json_decode(self.request.body)
        token = global_user_buffer.add_user(data)
        self.write({'token': token})