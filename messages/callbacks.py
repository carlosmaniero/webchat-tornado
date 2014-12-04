# coding: utf-8
from __future__ import unicode_literals
import time
from tornado import gen
from tornado.ioloop import IOLoop
from messages.buffer import global_message_buffer

# Buffer is aways a object
buffer = {}


@gen.coroutine
def save_messages():
    while True:
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 60)
        for webcast, item in global_message_buffer.items():
            messages = item.get_messages(buffer.get('cursor', None))

            if messages:
                buffer['cursor'] = messages[-1]['id']
                print(messages)