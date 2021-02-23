#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from kombu import Exchange
from namekox_core.core.friendly import AsLazyProperty
from namekox_amqp.core.consumer import BaseAMQPConsumer
from namekox_amqp.core.messaging import get_exchange_name
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.entrypoint import EntrypointProvider


class AMQPConsumer(BaseAMQPConsumer, SharedExtension, EntrypointProvider):
    @AsLazyProperty
    def exchange(self):
        service_name = self.container.service_cls.name
        exchange_name = get_exchange_name(service_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    def get_consumers(self, consumer_cls, channel):
        raise NotImplementedError
