#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import time
import socket


from kombu.common import maybe_declare
from namekox_amqp.core.messaging import (
    get_reply_queue_name,
    get_reply_route_name,
    get_exchange_name,
    get_reply_exchange_name,
    get_route_name,
)
from amqp.exceptions import ConnectionError
from kombu import Exchange, Queue, Consumer
from namekox_amqp.exceptions import RpcTimeout
from namekox_amqp.core.publisher import Publisher
from namekox_amqp.core.connection import AMQPConnect
from namekox_core.core.generator import generator_uuid
from namekox_core.exceptions import gen_data_to_exc, gen_exc_to_data
from namekox_core.core.friendly import AsLazyProperty, ignore_exception
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_SERIALIZE, DEFAULT_AMQP_RPC_TIMEOUT


class RpcStandaloneProxy(object):
    consumer = None
    producer = None
    connection = None

    def __init__(self, config, timeout=None, **push_options):
        self.config = config
        self.replystorage = {}
        self.push_options = push_options
        self.consumers_ident = generator_uuid()
        self.setup_producer()
        self.setup_connects()
        self.setup_consumer()
        self.timeout = timeout if isinstance(timeout, (int, float)) else None

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

    def setup_connects(self):
        self.connection = AMQPConnect(self.config).curobj

    def setup_producer(self):
        self.producer = Publisher(self.config)

    def on_message(self, body, message):
        correlation_id = message.properties.get('correlation_id', None)
        correlation_id and self.replystorage.update({correlation_id: body})
        message.ack()

    def setup_consumer(self):
        self.consumer and ignore_exception(self.consumer.close)
        channel = self.connection.channel()
        reply_n = self.get_reply_qn()
        reply_r = self.get_reply_rn()
        reply_e = Exchange(get_reply_exchange_name(), type='topic', durable=True, auto_delete=False)
        reply_e = reply_e.bind(channel)
        maybe_declare(reply_e, channel)
        reply_q = Queue(reply_n, exchange=reply_e, routing_key=reply_r, auto_delete=True)
        reply_q = reply_q.bind(channel)
        maybe_declare(reply_q, channel)
        consumer = Consumer(channel, queues=[reply_q], callbacks=[self.on_message], no_ack=False)
        consumer.qos(prefetch_count=1)
        consumer.consume()
        self.consumer = consumer

    def get_reply_rn(self, random_id=None):
        random_id = random_id or self.consumers_ident
        return get_reply_route_name('listener', 'cluster.rpc', random_id)

    def get_reply_qn(self, random_id=None):
        random_id = random_id or self.consumers_ident
        return get_reply_queue_name('listener', 'cluster.rpc', random_id)

    def __enter__(self):
        return RpcClusterProxy(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection and self.connection.release()


class RpcClusterProxy(object):
    def __init__(self, proxy):
        self.proxy = proxy

    def __call__(self, timeout=None, **push_options):
        self.proxy.push_options.update(push_options)
        self.proxy.timeout = timeout if isinstance(timeout, (int, float)) else None
        return self

    def __getattr__(self, service_name):
        return RpcServiceProxy(self.proxy, service_name)


class RpcServiceProxy(object):
    def __init__(self, proxy, service_name):
        self.proxy = proxy
        self.service_name = service_name

    def __getattr__(self, method_name):
        return RpcMethodProxy(self.proxy, self.service_name, method_name)


class RpcMethodProxy(object):
    def __init__(self, proxy, service_name, method_name):
        self.proxy = proxy
        self.method_name = method_name
        self.service_name = service_name

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    @property
    def serializer(self):
        return self.proxy.serializer

    @property
    def timeout(self):
        return self.proxy.timeout or self.proxy.rpctimeout

    @property
    def routekey(self):
        return get_route_name(self.service_name, self.method_name)

    @property
    def exchange(self):
        exchange_name = get_exchange_name(self.service_name)
        return Exchange(exchange_name, type='topic', durable=True, auto_delete=False)

    def raise_again(self, errs):
        raise gen_data_to_exc(errs)

    def call(self, *args, **kwargs):
        correlation_id, istimeout, ispublish, cur_time = generator_uuid(), False, False, time.time()
        while True:
            if correlation_id in self.proxy.replystorage:
                break
            if time.time() - cur_time > self.timeout:
                istimeout = True
                break
            try:
                self.proxy.connection.drain_events(timeout=0.01)
            except socket.error:
                self.proxy.connection.heartbeat_check()
                if ispublish is True:
                    continue
                message = {'args': args, 'kwargs': kwargs}
                self.pub_message(message, correlation_id)
                ispublish = True
                cur_time = time.time()
            except (IOError, ConnectionError):
                self.proxy.setup_producer()
                self.proxy.setup_connects()
                self.proxy.setup_consumer()
                ispublish = False
        if istimeout is True:
            errs = gen_exc_to_data(RpcTimeout(self.timeout))
            self.raise_again(errs)
        body = self.proxy.replystorage.pop(correlation_id)
        errs = body['errs']
        errs and self.raise_again(errs)
        return body['data']

    def call_sync(self, *args, **kwargs):
        correlation_id = generator_uuid()
        message = {'args': args, 'kwargs': kwargs}
        self.pub_message(message, correlation_id)

    def pub_message(self, message, correlation_id=None):
        correlation_id = correlation_id or generator_uuid()
        reply_r = self.proxy.get_reply_rn()
        push_options = self.proxy.push_options.copy()
        push_options['reply_to'] = reply_r
        push_options['exchange'] = self.exchange
        push_options['routing_key'] = self.routekey
        push_options['serializer'] = self.serializer
        push_options['correlation_id'] = correlation_id
        push_options.setdefault('expiration', self.timeout)
        self.proxy.producer.publish(message, **push_options)
