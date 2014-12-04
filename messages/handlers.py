# coding: utf-8
from __future__ import unicode_literals
import uuid
from tornado.gen import coroutine
from core.handlers import UserBaseHandler
from messages.buffer import get_message_buffer
from datetime import datetime


class MessageUpdatesHandler(UserBaseHandler):
    @coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)

        webcast = self.get_argument('webcast')
        buffer = get_message_buffer(webcast)

        self.future = buffer.add_waiter(cursor)

        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        webcast = self.get_argument('webcast')
        buffer = get_message_buffer(webcast)
        buffer.cancel_wait(self.future)


class MessageNewHandler(UserBaseHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
            "created_at": datetime.now(),
            "user": self.user
        }
        self.write(message)

        webcast = self.get_argument('webcast')
        buffer = get_message_buffer(webcast)
        buffer.new_message(message)