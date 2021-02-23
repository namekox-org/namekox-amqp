#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_amqp.core.proxy import RpcStandaloneProxy


class AMQPRpcProxy(object):
    def __init__(self, config):
        self.config = config
        self.proxy = RpcStandaloneProxy(config).get_instance()

    @classmethod
    def name(cls):
        return 'amqprpc'
