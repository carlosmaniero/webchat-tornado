# coding: utf-8
from __future__ import unicode_literals
from tornado.escape import json_decode
from tornado.options import options
from tornado.web import HTTPError
from core.handlers import ServerBaseHandler
from users.buffer import global_user_buffer
import json


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
        data = {
            'id': self.get_argument('id'),
            'first_name': self.get_argument('first_name'),
            'last_name': self.get_argument('last_name'),
            'nickname': self.get_argument('nickname'),
            'email': self.get_argument('email'),
            'thumb': self.get_argument('thumb')
        }

        if data['id'] is None or data['email'] is None:
            raise HTTPError(400, 'User need an id and a email')

        token = global_user_buffer.add_user(data)
        self.write({'token': token})
