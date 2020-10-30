#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from logging import getLogger
from kombu import Consumer, Queue
from namekox_core.core.friendly import as_wraps_partial
from namekox_amqp.core.entrypoints.consumer import AMQPConsumer
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_QOS
from namekox_amqp.core.messaging import get_queue_name, get_route_name


logger = getLogger(__name__)


class AMQPRpcConsumer(AMQPConsumer):
    def get_consumers(self, _, channel):
        self.consumers = []
        self.consumers_channels.add(channel)
        service_name = self.container.service_cls.name
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        maxqos = config.get('qos', DEFAULT_AMQP_QOS) or DEFAULT_AMQP_QOS
        for extension in self.extensions:
            queue_name = get_queue_name(service_name, extension.obj_name)
            route_keys = get_route_name(service_name, extension.obj_name)
            queue = Queue(queue_name, exchange=self.exchange, routing_key=route_keys, auto_delete=False)
            msg = '{} -LISTEN-> {} -BIND-> {}'.format(extension.obj_name, queue_name, self.exchange.name)
            logger.debug(msg)
            on_message = as_wraps_partial(self.on_message, extension)
            _channel = channel.connection.channel()
            self.consumers_channels.add(_channel)
            consumer = Consumer(_channel, queues=[queue], callbacks=[on_message])
            consumer.qos(prefetch_count=maxqos)
            self.consumers.append(consumer)
        return self.consumers
