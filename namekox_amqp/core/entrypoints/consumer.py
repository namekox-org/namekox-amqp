#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu import Exchange
from kombu.pools import connections
from namekox_amqp.core.connection import AMQPConnect
from namekox_amqp.core.consumer import BaseAMQPConsumer
from namekox_amqp.core.messaging import get_exchange_name
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.entrypoint import EntrypointProvider
from namekox_core.core.friendly import AsLazyProperty, ignore_exception


class AMQPConsumer(BaseAMQPConsumer, SharedExtension, EntrypointProvider):
    def stop(self):
        [ignore_exception(c.close) for c in self.consumers_channels]
        self.connection.release()

    @AsLazyProperty
    def exchange(self):
        service_name = self.container.service_cls.name
        exchange_name = get_exchange_name(service_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    @AsLazyProperty
    def connection(self):
        return AMQPConnect(self.container.config).curobj

    def get_consumers(self, consumer_cls, channel):
        raise NotImplementedError
