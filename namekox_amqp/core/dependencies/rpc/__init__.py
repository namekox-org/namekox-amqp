#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency
from namekox_amqp.core.messaging import get_reply_route_name
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_RPC_TIMEOUT, DEFAULT_AMQP_SERIALIZE


from .rpcproxy import RpcClusterProxy
from .listener import AMQPRpcListener


class AMQPRpcProxy(Dependency):
    listener = AMQPRpcListener()

    def __init__(self, timeout=None, **push_options):
        self.connect = None
        self.push_options = push_options
        self.timeout = timeout if isinstance(timeout, (int, float)) else None
        super(AMQPRpcProxy, self).__init__(**push_options)

    def setup(self):
        self.connect = AMQPConnect(self.container.config).instance

    @AsLazyProperty
    def producer(self):
        return self.connect.Producer()

    @AsLazyProperty
    def serializer(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    @AsLazyProperty
    def rpctimeout(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('rpc', {}).get('timeout', DEFAULT_AMQP_RPC_TIMEOUT) or DEFAULT_AMQP_RPC_TIMEOUT

    @AsLazyProperty
    def reply_route(self):
        service_name = self.container.service_cls.name
        return get_reply_route_name(service_name, self.listener.obj_name, self.listener.consumer.consumers_ident)

    def get_instance(self, context):
        return RpcClusterProxy(self, context)
