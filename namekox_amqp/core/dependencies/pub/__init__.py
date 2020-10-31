#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from logging import getLogger
from kombu.pools import producers
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE


logger = getLogger(__name__)


class AMQPPubProxy(Dependency):
    def __init__(self, exchange, **push_options):
        self.exchange = exchange
        push_options['exchange'] = exchange
        self.push_options = push_options
        super(AMQPPubProxy, self).__init__(exchange, **push_options)

    def stop(self):
        self.connection.release()

    @AsLazyProperty
    def connection(self):
        return AMQPConnect(self.container.config).curobj

    @AsLazyProperty
    def serializer(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    def send_async(self, message):
        push_options = self.push_options.copy()
        push_options.setdefault('serializer', self.serializer)
        with producers[self.connection].acquire(block=True) as producer:
            producer.publish(message, **push_options)
        msg = '{} send {} with {} succ'.format(self.obj_name, message, self.push_options)
        logger.debug(msg)
