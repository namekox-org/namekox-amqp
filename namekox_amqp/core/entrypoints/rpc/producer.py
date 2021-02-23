#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from kombu import Exchange
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_amqp.core.messaging import get_reply_exchange_name
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.entrypoint import EntrypointProvider
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE


class AMQPRpcProducer(SharedExtension, EntrypointProvider):
    def __init__(self, *args, **kwargs):
        self.connect = None
        super(AMQPRpcProducer, self).__init__(*args, **kwargs)

    def setup(self):
        self.connect = AMQPConnect(self.container.config).instance

    @AsLazyProperty
    def exchange(self):
        exchange_name = get_reply_exchange_name()
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    @AsLazyProperty
    def producer(self):
        return self.connect.Producer()

    @AsLazyProperty
    def serializer(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE
