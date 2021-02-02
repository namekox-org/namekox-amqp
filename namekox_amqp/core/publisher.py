#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from .connection import AMQPConnect


class Publisher(object):
    def __init__(self, config):
        self.config = config
        self.pusher = AMQPConnect(self.config).curobj.Producer()

    def publish(self, message, **push_options):
        self.pusher.publish(message, **push_options)
