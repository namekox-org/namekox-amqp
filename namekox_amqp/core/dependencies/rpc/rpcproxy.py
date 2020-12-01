#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu import Exchange
from logging import getLogger
from namekox_core.core.generator import generator_uuid
from namekox_amqp.core.messaging import get_exchange_name, get_route_name, gen_message_headers


from .rspproxy import RpcReplyProxy


logger = getLogger(__name__)


class RpcClusterProxy(object):
    def __init__(self, dependency, context):
        self.context = context
        self.dependency = dependency

    def __call__(self, timeout=None, **push_options):
        self.dependency.push_options.update(push_options)
        self.dependency.timeout = timeout if isinstance(timeout, (int, float)) else None
        return self

    def __getattr__(self, service_name):
        return RpcServiceProxy(self.dependency, self.context, service_name)


class RpcServiceProxy(object):
    def __init__(self, dependency, context, service_name):
        self.context = context
        self.dependency = dependency
        self.service_name = service_name

    def __getattr__(self, method_name):
        return RpcMethodProxy(self.dependency, self.context, self.service_name, method_name)


class RpcMethodProxy(object):
    def __init__(self, dependency, context, service_name, method_name):
        self.context = context
        self.dependency = dependency
        self.method_name = method_name
        self.service_name = service_name

    def __call__(self, *args, **kwargs):
        future = self.call_async(*args, **kwargs)
        return future.result()

    @property
    def listener(self):
        return self.dependency.listener

    @property
    def producer(self):
        return self.dependency.producer

    @property
    def serializer(self):
        return self.dependency.serializer

    @property
    def reply_to(self):
        return self.dependency.reply_route

    @property
    def routekey(self):
        return get_route_name(self.service_name, self.method_name)

    @property
    def timeout(self):
        return self.dependency.timeout or self.dependency.rpctimeout

    @property
    def exchange(self):
        exchange_name = get_exchange_name(self.service_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    def call_async(self, *args, **kwargs):
        message = {'args': args, 'kwargs': kwargs}
        correlation_id = generator_uuid()
        push_options = self.dependency.push_options.copy()
        push_options.update({
            'exchange': self.exchange,
            'reply_to': self.reply_to,
            'routing_key': self.routekey,
            'serializer': self.serializer,
            'correlation_id': correlation_id
        })
        push_options.setdefault('expiration', self.timeout)
        extr_headers = gen_message_headers(self.context.data)
        push_options.setdefault('headers', {}).update(extr_headers)
        self.producer.publish(message, **push_options)
        msg = '{} publish {} with {} succ'.format(self.dependency.obj_name, message, push_options)
        logger.debug(msg)
        reply_event = self.listener.get_reply_event(correlation_id, self.timeout)
        return RpcReplyProxy(reply_event)
