# coding: utf-8
from __future__ import unicode_literals
import simplejson as json
import time
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.ioloop import IOLoop
from messages.buffer import global_message_buffer

# Buffer is aways a object
import settings

buffer = {}


@gen.coroutine
def save_messages():
    while True:
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 60)

        messages_to_send = []

        for webcast, item in global_message_buffer.items():
            messages = item.get_messages(buffer.get('cursor', None))

            if messages:
                buffer['cursor'] = messages[-1]['id']
                for message in messages:
                    messages_to_send.append({
                        'webcast': webcast,
                        'user': message['user']['id'],
                        'body': message['body'],
                        'created_at': message['created_at']
                    })

        if messages_to_send:
            http_client = AsyncHTTPClient()
            yield http_client.fetch(HTTPRequest(url=settings.SAVE_MESSAGES_URL, method='POST', body=json.dumps({
                'key': settings.SAVE_MESSAGES_KEY,
                'messages': messages_to_send
            })))