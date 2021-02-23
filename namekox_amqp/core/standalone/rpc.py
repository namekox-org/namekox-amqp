#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import time
import socket


from kombu import Exchange, Queue
from namekox_amqp.constants import (
    AMQP_CONFIG_KEY,
    DEFAULT_AMQP_SERIALIZE,
    DEFAULT_AMQP_RPC_TIMEOUT,
    DEFAULT_AMQP_PUBLISHER_OPTIONS
)
from namekox_amqp.core.messaging import (
    get_reply_queue_name,
    get_reply_route_name,
    get_route_name,
    get_reply_exchange_name,
    get_exchange_name
)
from namekox_amqp.exceptions import RpcTimeout
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.generator import generator_uuid
from namekox_core.exceptions import gen_data_to_exc, gen_exc_to_data


class RpcStandaloneProxy(object):
    def __init__(self, config, timeout=None, **push_options):
        self.config = config
        self.push_options = push_options
        self.replies_storage = {}
        self.consumers_ident = generator_uuid()
        self.timeout = timeout if isinstance(timeout, (int, float)) else None

    @AsLazyProperty
    def connect(self):
        return AMQPConnect(self.config).instance

    @AsLazyProperty
    def serializer(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('serializer', DEFAULT_AMQP_SERIALIZE) or DEFAULT_AMQP_SERIALIZE

    @AsLazyProperty
    def rpctimeout(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('rpc', {}).get('timeout', DEFAULT_AMQP_RPC_TIMEOUT) or DEFAULT_AMQP_RPC_TIMEOUT

    def get_instance(self):
        return RpcClusterProxy(self)

    def on_message(self, body, message):
        correlation_id = message.properties.get('correlation_id', None)
        correlation_id and self.replies_storage.update({correlation_id: body})
        message.ack()

    def get_reply_rn(self, random_id=None):
        random_id = random_id or self.consumers_ident
        return get_reply_route_name('listener', 'cluster.rpc', random_id)

    def get_reply_qn(self, random_id=None):
        random_id = random_id or self.consumers_ident
        return get_reply_queue_name('listener', 'cluster.rpc', random_id)


class RpcClusterProxy(object):
    def __init__(self, proxy):
        self.proxy = proxy

    def __call__(self, timeout=None, **push_options):
        self.proxy.push_options.update(push_options)
        self.proxy.timeout = timeout if isinstance(timeout, (int, float)) else None
        return self

    def __getattr__(self, s_name):
        return RpcServiceProxy(self.proxy, s_name)


class RpcServiceProxy(object):
    def __init__(self, proxy, s_name):
        self.proxy = proxy
        self.s_name = s_name

    def __getattr__(self, m_name):
        return RpcMethodProxy(self.proxy, self.s_name, m_name)


class RpcMethodProxy(object):
    def __init__(self, proxy, s_name, m_name):
        self.proxy = proxy
        self.m_name = m_name
        self.s_name = s_name

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    @property
    def connect(self):
        return self.proxy.connect

    @property
    def serializer(self):
        return self.proxy.serializer

    @property
    def reply_to(self):
        return self.proxy.get_reply_rn()

    @property
    def timeout(self):
        return self.proxy.timeout or self.proxy.rpctimeout

    @property
    def routekey(self):
        return get_route_name(self.s_name, self.m_name)

    @property
    def exchange(self):
        exchange_name = get_exchange_name(self.s_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    def raise_again(self, errs):
        raise gen_data_to_exc(errs)

    def call(self, *args, **kwargs):
        with AMQPConnect(self.proxy.config).instance as c:
            reply_n = self.proxy.get_reply_qn()
            reply_r = self.proxy.get_reply_rn()
            reply_e = Exchange(get_reply_exchange_name(), type='topic', durable=True, auto_delete=False)
            reply_q = Queue(reply_n, exchange=reply_e, routing_key=reply_r, auto_delete=True)
            with c.Consumer(queues=[reply_q], callbacks=[self.proxy.on_message], no_ack=False):
                correlation_id, istimeout, ispublish, cur_time = generator_uuid(), False, False, time.time()
                count, sleep = 0, 0.01
                while True:
                    if correlation_id in self.proxy.replies_storage:
                        break
                    if time.time() - cur_time > self.timeout:
                        istimeout = True
                        break
                    try:
                        c.drain_events(timeout=sleep)
                    except socket.error:
                        count += sleep
                        count % 2 == 0 and c.heartbeat_check()
                        if ispublish is True:
                            continue
                        message = {'args': args, 'kwargs': kwargs}
                        self.send_sync(message, correlation_id)
                        ispublish = True
                        cur_time = time.time()
                if istimeout is True:
                    errs = gen_exc_to_data(RpcTimeout(self.timeout))
                    self.raise_again(errs)
                body = self.proxy.replies_storage.pop(correlation_id)
                errs = body['errs']
                errs and self.raise_again(errs)
                return body['data']

    def call_sync(self, *args, **kwargs):
        correlation_id = generator_uuid()
        message = {'args': args, 'kwargs': kwargs}
        self.send_sync(message, correlation_id)

    def send_sync(self, mesg, c_id=None):
        correlation_id = c_id or generator_uuid()
        push_options = DEFAULT_AMQP_PUBLISHER_OPTIONS.copy()
        push_options.update(self.proxy.push_options)
        push_options.update({'reply_to': self.reply_to,
                             'exchange': self.exchange,
                             'routing_key': self.routekey,
                             'serializer': self.serializer,
                             'correlation_id': correlation_id})
        push_options.setdefault('expiration', self.timeout)
        self.connect.Producer().publish(mesg, **push_options)
