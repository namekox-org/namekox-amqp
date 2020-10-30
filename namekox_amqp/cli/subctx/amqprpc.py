#! -*- coding: utf-8 -*-

# author: forcemain@163.com


class AMQPRpcProxy(object):
    def __init__(self, config):
        self.config = config

    @classmethod
    def name(cls):
        return 'amqprpc'
