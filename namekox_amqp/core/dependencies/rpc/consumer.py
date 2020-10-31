#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from logging import getLogger
from kombu.pools import connections
from kombu import Exchange, Consumer, Queue
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.generator import generator_uuid
from namekox_amqp.core.consumer import BaseAMQPConsumer
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.dependency import DependencyProvider
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_QOS
from namekox_core.core.friendly import as_wraps_partial, ignore_exception
from namekox_amqp.core.messaging import get_reply_exchange_name, get_reply_queue_name, get_reply_route_name


logger = getLogger(__name__)


class AMQPReplyConsumer(BaseAMQPConsumer, SharedExtension, DependencyProvider):
    def __init__(self, *args, **kwargs):
        self.consumers_ident = generator_uuid()
        super(AMQPReplyConsumer, self).__init__(*args, **kwargs)

    def stop(self):
        [ignore_exception(c.close) for c in self.consumers_channels]
        self.connection.release()

    @AsLazyProperty
    def exchange(self):
        exchange_name = get_reply_exchange_name()
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    @AsLazyProperty
    def connection(self):
        return AMQPConnect(self.container.config).curobj

    def get_consumers(self, _, channel):
        self.consumers = []
        self.consumers_channels.add(channel)
        service_name = self.container.service_cls.name
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        maxqos = config.get('qos', DEFAULT_AMQP_QOS) or DEFAULT_AMQP_QOS
        for extension in self.extensions:
            queue_name = get_reply_queue_name(service_name, extension.obj_name, self.consumers_ident)
            route_keys = get_reply_route_name(service_name, extension.obj_name, self.consumers_ident)
            queue = Queue(queue_name, exchange=self.exchange, routing_key=route_keys, auto_delete=True)
            msg = '{} -LISTEN-> {} -BIND-> {}'.format(extension.obj_name, queue_name, self.exchange.name)
            logger.debug(msg)
            on_message = as_wraps_partial(self.on_message, extension)
            _channel = channel.connection.channel()
            self.consumers_channels.add(_channel)
            consumer = Consumer(_channel, queues=[queue], callbacks=[on_message])
            consumer.qos(prefetch_count=maxqos)
            self.consumers.append(consumer)
        return self.consumers
