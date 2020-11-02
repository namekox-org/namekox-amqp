#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from .connection import AMQPConnect


class Publisher(object):
    def __init__(self, config):
        self.config = config

    def publish(self, message, **push_options):
        c = AMQPConnect(self.config).curobj
        p = c.Producer()
        p.publish(message, **push_options)
        p.release()
        c.release()
