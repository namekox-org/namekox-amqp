#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from kombu import Exchange
from logging import getLogger
from namekox_core.core.generator import generator_uuid
from namekox_amqp.constants import DEFAULT_AMQP_PUBLISHER_OPTIONS
from namekox_amqp.core.messaging import get_exchange_name, get_route_name, gen_message_headers


from .rspproxy import RpcReplyProxy


logger = getLogger(__name__)


class RpcClusterProxy(object):
    def __init__(self, ext, ctx):
        self.ctx = ctx
        self.ext = ext

    def __call__(self, timeout=None, **push_options):
        self.ext.push_options.update(push_options)
        self.ext.timeout = timeout if isinstance(timeout, (int, float)) else None
        return self

    def __getattr__(self, s_name):
        return RpcServiceProxy(self.ext, self.ctx, s_name)


class RpcServiceProxy(object):
    def __init__(self, ext, ctx, s_name):
        self.ctx = ctx
        self.ext = ext
        self.s_name = s_name

    def __getattr__(self, m_name):
        return RpcMethodProxy(self.ext, self.ctx, self.s_name, m_name)


class RpcMethodProxy(object):
    def __init__(self, ext, ctx, s_name, m_name):
        self.ctx = ctx
        self.ext = ext
        self.m_name = m_name
        self.s_name = s_name

    def __call__(self, *args, **kwargs):
        future = self.call_async(*args, **kwargs)
        return future.result()

    @property
    def listener(self):
        return self.ext.listener

    @property
    def connect(self):
        return self.ext.connect

    @property
    def producer(self):
        return self.ext.producer

    @property
    def serializer(self):
        return self.ext.serializer

    @property
    def reply_to(self):
        return self.ext.reply_route

    @property
    def routekey(self):
        return get_route_name(self.s_name, self.m_name)

    @property
    def timeout(self):
        return self.ext.timeout or self.ext.rpctimeout

    @property
    def exchange(self):
        exchange_name = get_exchange_name(self.s_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    def call_async(self, *args, **kwargs):
        message = {'args': args, 'kwargs': kwargs}
        correlation_id = generator_uuid()
        push_options = DEFAULT_AMQP_PUBLISHER_OPTIONS.copy()
        push_options.update(self.ext.push_options)
        push_options.update({
            'exchange': self.exchange,
            'reply_to': self.reply_to,
            'routing_key': self.routekey,
            'serializer': self.serializer,
            'correlation_id': correlation_id
        })
        push_options.setdefault('expiration', self.timeout)
        extr_headers = gen_message_headers(self.ctx.data)
        push_options.setdefault('headers', {})
        push_options['headers'].update(extr_headers)
        self.producer.publish(message, **push_options)
        logger.debug('{} publish {} with {}'.format(self.ext.obj_name, message, push_options))
        return RpcReplyProxy(self.listener.get_reply_event(correlation_id, self.timeout))
