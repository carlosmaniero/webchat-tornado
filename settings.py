# coding: utf-8
from tornado.options import define

define('allowed_hosts', default=['127.0.0.1'])
define('debug', default=False)

SAVE_MESSAGES_KEY = 'xxx'
SAVE_MESSAGES_URL = 'http://localhost:8000/api/chat/save-messages/'