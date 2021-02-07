# Install
```shell script
pip install -U namekox-amqp
```

# Example
> ping.py
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


import time
import random


from kombu import Exchange
from namekox_amqp.core.entrypoints import amqp
from namekox_timer.core.entrypoints.timer import timer
from namekox_amqp.core.dependencies.rpc import AMQPRpcProxy
from namekox_amqp.core.dependencies.pub import AMQPPubProxy


class Ping(object):
    name = 'ping'

    rpc = AMQPRpcProxy()
    pub = AMQPPubProxy(Exchange('e-pub', 'topic'), routing_key='r-pub')

    @amqp.rpc()
    def rpc_ping(self, data):
        resp = self.rpc(timeout=5).ping.rpc_pong(data)
        return {'rpc_ping_recv': resp}

    @amqp.rpc()
    def rpc_pong(self, data):
        # time.sleep(10)
        return {'rpc_pong_recv': data}

    @amqp.sub(Exchange('e-pub', 'topic'), routing_key='r-pub')
    def amq_sub(self, body):
        return {'amq_sub_recv': body}

    @timer(1)
    def test_me(self):
        v = random.randint(1, 100)
        d = {'test_me_send': v}
        self.pub.send_async(d)
        self.rpc.ping.rpc_ping(d)
```

# Running
> config.yaml
```yaml
AMQP:
  qos: 50
  ssl: ~
  rpc:
    timeout: 20
  transport: ~
  heartbeat: 60
  serializer: json
  uri: pyamqp://admin:nimda@127.0.0.1:5672//
```

> namekox run ping
```shell script
2020-11-02 16:07:41,771 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-02 16:07:41,779 DEBUG starting services ['ping']
2020-11-02 16:07:41,779 DEBUG starting service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer]
2020-11-02 16:07:41,780 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-11-02 16:07:41,780 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-02 16:07:41,781 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-11-02 16:07:41,805 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:41,815 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:41,821 DEBUG Open OK!
2020-11-02 16:07:41,822 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-11-02 16:07:41,822 DEBUG using channel_id: 1
2020-11-02 16:07:41,824 DEBUG Open OK!
2020-11-02 16:07:41,824 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-11-02 16:07:41,825 DEBUG using channel_id: 1
2020-11-02 16:07:41,828 DEBUG Channel open
2020-11-02 16:07:41,829 DEBUG amq_sub -LISTEN-> namekox-q-ping-amq_sub -BIND-> e-pub
2020-11-02 16:07:41,829 DEBUG using channel_id: 2
2020-11-02 16:07:41,829 DEBUG Channel open
2020-11-02 16:07:41,830 DEBUG rpc_ping -LISTEN-> namekox-q-ping-rpc_ping -BIND-> namekox-e-ping
2020-11-02 16:07:41,830 DEBUG using channel_id: 2
2020-11-02 16:07:41,832 DEBUG Channel open
2020-11-02 16:07:41,833 DEBUG Channel open
2020-11-02 16:07:41,843 DEBUG rpc_pong -LISTEN-> namekox-q-ping-rpc_pong -BIND-> namekox-e-ping
2020-11-02 16:07:41,843 DEBUG using channel_id: 3
2020-11-02 16:07:41,847 DEBUG Channel open
2020-11-02 16:07:41,850 DEBUG amqp consumers ready.
2020-11-02 16:07:41,862 DEBUG amqp consumers ready.
2020-11-02 16:07:41,862 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer] started
2020-11-02 16:07:41,862 DEBUG starting service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener]
2020-11-02 16:07:41,863 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-11-02 16:07:41,873 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:41,880 DEBUG Open OK!
2020-11-02 16:07:41,880 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-11-02 16:07:41,881 DEBUG using channel_id: 1
2020-11-02 16:07:41,885 DEBUG Channel open
2020-11-02 16:07:41,885 DEBUG listener -LISTEN-> namekox-rq-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a -BIND-> namekox-re-global
2020-11-02 16:07:41,886 DEBUG using channel_id: 2
2020-11-02 16:07:41,889 DEBUG Channel open
2020-11-02 16:07:41,916 DEBUG amqp consumers ready.
2020-11-02 16:07:41,917 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener] started
2020-11-02 16:07:41,917 DEBUG services ['ping'] started
2020-11-02 16:07:42,791 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2020-11-02 16:07:42,809 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:42,815 DEBUG Open OK!
2020-11-02 16:07:42,815 DEBUG using channel_id: 1
2020-11-02 16:07:42,819 DEBUG Channel open
2020-11-02 16:07:42,825 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 90}, <kombu.transport.pyamqp.Message object at 0x10e6bb5a8>), kwargs={}, tid=handle_message)
2020-11-02 16:07:42,825 DEBUG Closed channel #1
2020-11-02 16:07:42,826 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 90},), kwargs={}, context={})
2020-11-02 16:07:42,827 DEBUG pub send {'test_me_send': 90} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2020-11-02 16:07:42,849 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:42,859 DEBUG Open OK!
2020-11-02 16:07:42,859 DEBUG using channel_id: 1
2020-11-02 16:07:42,864 DEBUG Channel open
2020-11-02 16:07:42,868 DEBUG Closed channel #1
2020-11-02 16:07:42,871 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 90}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10e6bb5a8>), kwargs={}, tid=handle_message)
2020-11-02 16:07:42,871 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 90}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'ccd85cdf-f9c6-4254-9435-f090328d6191', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'expiration': u'20000'}
2020-11-02 16:07:42,871 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 90}], kwargs={}, context={})
2020-11-02 16:07:42,880 DEBUG rpc publish {'args': ({'test_me_send': 90},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_ping', 'headers': {}, 'correlation_id': 'ccd85cdf-f9c6-4254-9435-f090328d6191', 'expiration': 20, 'reply_to': 'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json'} succ
2020-11-02 16:07:42,888 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:42,898 DEBUG Open OK!
2020-11-02 16:07:42,899 DEBUG using channel_id: 1
2020-11-02 16:07:42,902 DEBUG Channel open
2020-11-02 16:07:42,905 DEBUG Closed channel #1
2020-11-02 16:07:42,906 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 90}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10e6bb640>), kwargs={}, tid=handle_message)
2020-11-02 16:07:42,906 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 90}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'9debef6f-ca4d-410b-8221-f1e51e423ff8', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'expiration': u'5000'}
2020-11-02 16:07:42,907 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 90}], kwargs={}, context={})
2020-11-02 16:07:42,919 DEBUG rpc publish {'args': ({u'test_me_send': 90},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_pong', 'headers': {}, 'correlation_id': '9debef6f-ca4d-410b-8221-f1e51e423ff8', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json'} succ
2020-11-02 16:07:42,927 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:42,933 DEBUG Open OK!
2020-11-02 16:07:42,933 DEBUG using channel_id: 1
2020-11-02 16:07:42,936 DEBUG Channel open
2020-11-02 16:07:42,939 DEBUG Closed channel #1
2020-11-02 16:07:42,944 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 90}}} with {'correlation_id': u'9debef6f-ca4d-410b-8221-f1e51e423ff8', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-11-02 16:07:42,960 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 90}}}, <kombu.transport.pyamqp.Message object at 0x10e6bb640>), kwargs={}, tid=handle_message)
2020-11-02 16:07:42,961 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 90}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'9debef6f-ca4d-410b-8221-f1e51e423ff8', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
2020-11-02 16:07:42,975 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:42,980 DEBUG Open OK!
2020-11-02 16:07:42,980 DEBUG using channel_id: 1
2020-11-02 16:07:42,983 DEBUG Channel open
2020-11-02 16:07:42,986 DEBUG Closed channel #1
2020-11-02 16:07:42,987 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 90}}}}, <kombu.transport.pyamqp.Message object at 0x10e6bb640>), kwargs={}, tid=handle_message)
2020-11-02 16:07:42,989 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 90}}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'ccd85cdf-f9c6-4254-9435-f090328d6191', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'20000'}
2020-11-02 16:07:42,990 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 90}}}} with {'correlation_id': u'ccd85cdf-f9c6-4254-9435-f090328d6191', 'expiration': 20, 'routing_key': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-11-02 16:07:43,792 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2020-11-02 16:07:43,810 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:43,817 DEBUG Open OK!
2020-11-02 16:07:43,817 DEBUG using channel_id: 1
2020-11-02 16:07:43,826 DEBUG Channel open
2020-11-02 16:07:43,828 DEBUG Closed channel #1
2020-11-02 16:07:43,829 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 69}, <kombu.transport.pyamqp.Message object at 0x10e6bb5a8>), kwargs={}, tid=handle_message)
2020-11-02 16:07:43,830 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 69},), kwargs={}, context={})
2020-11-02 16:07:43,832 DEBUG pub send {'test_me_send': 69} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2020-11-02 16:07:43,850 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:43,860 DEBUG Open OK!
2020-11-02 16:07:43,860 DEBUG using channel_id: 1
2020-11-02 16:07:43,864 DEBUG Channel open
2020-11-02 16:07:43,868 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 69}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10e6bb5a8>), kwargs={}, tid=handle_message)
2020-11-02 16:07:43,868 DEBUG Closed channel #1
2020-11-02 16:07:43,869 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 69}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'17916fef-375d-46dd-b5e1-f20a510ca541', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'expiration': u'5000'}
2020-11-02 16:07:43,869 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 69}], kwargs={}, context={})
2020-11-02 16:07:43,879 DEBUG rpc publish {'args': ({'test_me_send': 69},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_ping', 'headers': {}, 'correlation_id': '17916fef-375d-46dd-b5e1-f20a510ca541', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json'} succ
2020-11-02 16:07:43,889 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:43,899 DEBUG Open OK!
2020-11-02 16:07:43,899 DEBUG using channel_id: 1
2020-11-02 16:07:43,902 DEBUG Channel open
2020-11-02 16:07:43,913 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 69}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10e6bb640>), kwargs={}, tid=handle_message)
2020-11-02 16:07:43,913 DEBUG Closed channel #1
2020-11-02 16:07:43,913 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 69}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'b9122e40-0a3c-4647-b6f2-a317e82ba1f8', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'expiration': u'5000'}
2020-11-02 16:07:43,913 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 69}], kwargs={}, context={})
2020-11-02 16:07:43,922 DEBUG rpc publish {'args': ({u'test_me_send': 69},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_pong', 'headers': {}, 'correlation_id': 'b9122e40-0a3c-4647-b6f2-a317e82ba1f8', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json'} succ
2020-11-02 16:07:43,930 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:43,936 DEBUG Open OK!
2020-11-02 16:07:43,936 DEBUG using channel_id: 1
2020-11-02 16:07:43,939 DEBUG Channel open
2020-11-02 16:07:43,946 DEBUG Closed channel #1
2020-11-02 16:07:43,947 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 69}}}, <kombu.transport.pyamqp.Message object at 0x10e6bb6d8>), kwargs={}, tid=handle_message)
2020-11-02 16:07:43,947 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 69}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'b9122e40-0a3c-4647-b6f2-a317e82ba1f8', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
2020-11-02 16:07:43,955 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 69}}} with {'correlation_id': u'b9122e40-0a3c-4647-b6f2-a317e82ba1f8', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-11-02 16:07:43,962 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:07:43,967 DEBUG Open OK!
2020-11-02 16:07:43,967 DEBUG using channel_id: 1
2020-11-02 16:07:43,969 DEBUG Channel open
2020-11-02 16:07:43,972 DEBUG Closed channel #1
2020-11-02 16:07:43,973 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 69}}}}, <kombu.transport.pyamqp.Message object at 0x10e6bb640>), kwargs={}, tid=handle_message)
2020-11-02 16:07:43,973 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 69}}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'17916fef-375d-46dd-b5e1-f20a510ca541', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
2020-11-02 16:07:43,976 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 69}}}} with {'correlation_id': u'17916fef-375d-46dd-b5e1-f20a510ca541', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.7a94a279-4080-4071-9fcf-c3b5811a7b5a', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
^C2020-11-02 16:07:44,470 DEBUG stopping services ['ping']
2020-11-02 16:07:44,471 DEBUG stopping service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer]
2020-11-02 16:07:44,472 DEBUG wait service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer] stop
2020-11-02 16:07:44,472 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer] stopped
2020-11-02 16:07:44,472 DEBUG stopping service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener]
2020-11-02 16:07:44,473 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener] stopped
2020-11-02 16:07:44,477 DEBUG services ['ping'] stopped
2020-11-02 16:07:44,478 DEBUG killing services ['ping']
2020-11-02 16:07:44,479 DEBUG service ping already stopped
2020-11-02 16:07:44,480 DEBUG services ['ping'] killed
```

# Integrate
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


import time
import random


from namekox_amqp.core.standalone.rpc import RpcStandaloneProxy


if __name__ == '__main__':
    config = {'AMQP': {'qos': 1, 'ssl': None,
                       'heartbeat': 15,
                       'transport': None,
                       'serializer': 'json',
                       'rpc': {'timeout': 20},
                       'uri': 'pyamqp://admin:nimda@127.0.0.1:5672//'}}
    cur_time = time.time()
    p = RpcStandaloneProxy(config).get_instance()
    val = random.randint(1, 100)
    res = p(timeout=1).ping.rpc_ping(val)
    print('Got cluster rpc result: {}, cost: {}s'.format(res, time.time()-cur_time))
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_amqp.cli.subctx.amqprpc:AMQPRpcProxy
  - namekox_amqp.cli.subctx.amqppub:AMQPPubProxy
AMQP:
  qos: 50
  ssl: ~
  rpc:
    timeout: 20
  transport: ~
  heartbeat: 60
  serializer: json
  uri: pyamqp://admin:nimda@127.0.0.1:5672//
```

> namekox shell
```shell script
2020-11-02 16:13:06,473 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:13:06,479 DEBUG Open OK!
2020-11-02 16:13:06,479 DEBUG using channel_id: 1
2020-11-02 16:13:06,481 DEBUG Channel open
Namekox Python 2.7.16 (default, Dec 13 2019, 18:00:32)
[GCC 4.2.1 Compatible Apple LLVM 11.0.0 (clang-1100.0.32.4) (-macos10.15-objc-s shell on darwin
In [1]: nx.amqprpc.proxy.ping.rpc_ping('nb')
2020-11-02 16:13:08,841 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:13:08,848 DEBUG Open OK!
2020-11-02 16:13:08,848 DEBUG using channel_id: 1
2020-11-02 16:13:08,857 DEBUG Channel open
2020-11-02 16:13:08,863 DEBUG Closed channel #1
Out[1]: {u'rpc_ping_recv': u'nb'}

In [3]: from kombu import Exchange

In [4]: nx.amqppub.proxy(Exchange('e-pub', 'topic'), routing_key='r-pub').send_async({'nb': True})
2020-11-02 16:14:02,612 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-11-02 16:14:02,619 DEBUG Open OK!
2020-11-02 16:14:02,619 DEBUG using channel_id: 1
2020-11-02 16:14:02,623 DEBUG Channel open
2020-11-02 16:14:02,625 DEBUG Closed channel #1
2020-11-02 16:14:02,628 DEBUG cluster.pub send {'nb': True} with {'routing_key': 'r-pub', 'serializer': 'json', 'exchange': <unbound Exchange e-pub(topic)>} succ
```
