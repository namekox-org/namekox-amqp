#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from logging import getLogger
from kombu.pools import producers
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE


logger = getLogger(__name__)


class PubStandaloneProxy(object):
    def __init__(self, config, exchange=None, **push_options):
        self.config = config
        self.exchange = exchange
        exchange and push_options.update({'exchange': exchange})
        self.push_options = push_options

    @AsLazyProperty
    def connection(self):
        return AMQPConnect(self.config).curobj

    @AsLazyProperty
    def serializer(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    def get_instance(self):
        return PubClusterProxy(self)

    def __enter__(self):
        return PubClusterProxy(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.release()


class PubClusterProxy(object):
    def __init__(self, proxy):
        self.proxy = proxy

    def __call__(self, exchange, **push_options):
        self.proxy.exchange = exchange
        self.proxy.push_options.update(push_options)
        self.proxy.push_options['exchange'] = exchange
        return self

    @property
    def serializer(self):
        return self.proxy.serializer

    @property
    def connection(self):
        return self.proxy.connection

    def send_async(self, message):
        push_options = self.proxy.push_options.copy()
        push_options.setdefault('serializer', self.serializer)
        with producers[self.connection].acquire(block=True) as producer:
            producer.publish(message, **push_options)
        msg = 'cluster.pub send {} with {} succ'.format(message, push_options)
        logger.debug(msg)
