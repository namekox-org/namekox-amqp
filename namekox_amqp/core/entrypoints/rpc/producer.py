#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu import Exchange
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_amqp.core.messaging import get_reply_exchange_name
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.entrypoint import EntrypointProvider
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE


class AMQPRpcProducer(SharedExtension, EntrypointProvider):
    def __init__(self, *args, **kwargs):
        super(AMQPRpcProducer, self).__init__(*args, **kwargs)

    def stop(self):
        self.connection.release()

    @AsLazyProperty
    def exchange(self):
        exchange_name = get_reply_exchange_name()
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    @AsLazyProperty
    def connection(self):
        return AMQPConnect(self.container.config).curobj

    @AsLazyProperty
    def serializer(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE
