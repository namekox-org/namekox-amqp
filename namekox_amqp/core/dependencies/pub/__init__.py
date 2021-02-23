#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency
from namekox_amqp.core.messaging import gen_message_headers
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE, DEFAULT_AMQP_PUBLISHER_OPTIONS


logger = getLogger(__name__)


class AMQPPubProxy(Dependency):
    def __init__(self, exchange, **push_options):
        self.context = None
        self.exchange = exchange
        self.connect = None
        push_options['exchange'] = exchange
        self.push_options = push_options
        super(AMQPPubProxy, self).__init__(exchange, **push_options)

    def setup(self):
        self.connect = AMQPConnect(self.container.config).instance

    @AsLazyProperty
    def producer(self):
        return self.connect.Producer()

    @AsLazyProperty
    def serializer(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    def get_instance(self, context):
        self.context = context
        return self

    def send_async(self, message):
        push_options = DEFAULT_AMQP_PUBLISHER_OPTIONS.copy()
        push_options.update(self.push_options)
        push_options.setdefault('serializer', self.serializer)
        extr_headers = gen_message_headers(self.context.data)
        push_options.setdefault('headers', {})
        push_options['headers'].update(extr_headers)
        self.producer.publish(message, **push_options)
        logger.debug('{} send {} with {} succ'.format(self.obj_name, message, self.push_options))
