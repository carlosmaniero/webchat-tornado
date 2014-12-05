# coding: utf-8
from __future__ import unicode_literals
from tornado.concurrent import Future


class MessageBuffer(object):

    def __init__(self, webcast, **kwargs):
        self.waiters = set()
        self.messages = []
        self.webcast = webcast
        self.cache_size = kwargs.get('cache_size', 20)

    def add_waiter(self, cursor=None):
        result_future = Future()
        if cursor:
            new_count = 0
            for msg in reversed(self.messages):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                result_future.set_result(self.messages[-new_count:])
                return result_future
        elif self.messages:
            result_future.set_result(self.messages[self.cache_size:])
            return result_future

        self.waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.waiters.remove(future)
        future.set_result([])

    def new_message(self, message):
        for future in self.waiters:
            future.set_result([message])
        self.waiters = set()
        self.messages.append(message)

    def get_messages(self, cursor):
        messages = self.messages
        if cursor:
            new_count = 0
            for msg in reversed(messages):
                if msg["id"] == cursor:
                    break
                new_count += 1
            if new_count:
                messages = messages[-new_count:]
        self.messages = self.messages[-self.cache_size:]
        return messages


global_message_buffer = {}


def get_message_buffer(webcast):
    buffer = global_message_buffer.get(webcast)

    if buffer is None:
        buffer = global_message_buffer[webcast] = MessageBuffer(webcast)

    return buffer