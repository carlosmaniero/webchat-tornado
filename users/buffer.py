# coding: utf-8
from __future__ import unicode_literals
import uuid
from tornado.web import HTTPError


class UserBuffer(object):

    def __init__(self):
        self.users = {}

    def add_user(self, user):
        for key, item in self.users.items():
            if item['id'] == user['id']:
                self.users[key] = user
                return key

        token = str(uuid.uuid4())
        self.users[token] = user
        return token

    def get_user(self, token):
        try:
            return self.users[token]
        except KeyError:
            raise HTTPError(403, "Token not found!")


global_user_buffer = UserBuffer()