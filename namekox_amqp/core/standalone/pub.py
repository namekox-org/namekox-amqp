#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE, DEFAULT_AMQP_PUBLISHER_OPTIONS


logger = getLogger(__name__)


class PubStandaloneProxy(object):
    def __init__(self, config, exchange=None, **push_options):
        self.config = config
        self.exchange = exchange
        self.connect = AMQPConnect(config).instance
        exchange and push_options.update({'exchange': exchange})
        self.push_options = push_options

    @AsLazyProperty
    def producer(self):
        return self.connect.Producer()

    @AsLazyProperty
    def serializer(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    def get_instance(self):
        return PubClusterProxy(self)

    def __enter__(self):
        return PubClusterProxy(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.release()


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
    def connect(self):
        return self.proxy.connect

    @property
    def producer(self):
        return self.proxy.producer

    def send_async(self, message):
        push_options = DEFAULT_AMQP_PUBLISHER_OPTIONS.copy()
        push_options.update(self.proxy.push_options)
        push_options.setdefault('serializer', self.serializer)
        self.producer.publish(message, **push_options)
        logger.debug('cluster.pub send {} with {} succ'.format(message, push_options))
