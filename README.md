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


SERVICE_NAME = 'ping'


class Ping(object):
    name = SERVICE_NAME
    description = u'PING服务'

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
  uri: pyamqp://admin:nimda@127.0.0.1:5672//
```

> namekox run ping
```shell script
2021-02-08 10:47:35,822 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-02-08 10:47:35,824 DEBUG starting services ['ping']
2021-02-08 10:47:35,824 DEBUG starting service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer]
2021-02-08 10:47:35,828 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2021-02-08 10:47:35,828 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2021-02-08 10:47:35,828 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2021-02-08 10:47:35,851 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:35,860 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2021-02-08 10:47:35,861 DEBUG using channel_id: 1
2021-02-08 10:47:35,863 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:35,867 DEBUG Channel open
2021-02-08 10:47:35,867 DEBUG rpc_ping -LISTEN-> namekox-q-ping-rpc_ping -BIND-> namekox-e-ping
2021-02-08 10:47:35,867 DEBUG using channel_id: 2
2021-02-08 10:47:35,870 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2021-02-08 10:47:35,871 DEBUG using channel_id: 1
2021-02-08 10:47:35,875 DEBUG Channel open
2021-02-08 10:47:35,877 DEBUG Channel open
2021-02-08 10:47:35,878 DEBUG amq_sub -LISTEN-> namekox-q-ping-amq_sub -BIND-> e-pub
2021-02-08 10:47:35,878 DEBUG using channel_id: 2
2021-02-08 10:47:35,885 DEBUG Channel open
2021-02-08 10:47:35,891 DEBUG rpc_pong -LISTEN-> namekox-q-ping-rpc_pong -BIND-> namekox-e-ping
2021-02-08 10:47:35,891 DEBUG using channel_id: 3
2021-02-08 10:47:35,896 DEBUG Channel open
2021-02-08 10:47:35,903 DEBUG amqp consumers ready.
2021-02-08 10:47:35,913 DEBUG amqp consumers ready.
2021-02-08 10:47:35,914 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer] started
2021-02-08 10:47:35,914 DEBUG starting service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc]
2021-02-08 10:47:35,916 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2021-02-08 10:47:35,933 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:35,940 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2021-02-08 10:47:35,940 DEBUG using channel_id: 1
2021-02-08 10:47:35,944 DEBUG Channel open
2021-02-08 10:47:35,944 DEBUG listener -LISTEN-> namekox-rq-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070 -BIND-> namekox-re-global
2021-02-08 10:47:35,944 DEBUG using channel_id: 2
2021-02-08 10:47:35,948 DEBUG Channel open
2021-02-08 10:47:35,982 DEBUG amqp consumers ready.
2021-02-08 10:47:35,982 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc] started
2021-02-08 10:47:35,983 DEBUG services ['ping'] started
2021-02-08 10:47:36,836 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2021-02-08 10:47:36,851 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:36,866 DEBUG using channel_id: 1
2021-02-08 10:47:36,868 DEBUG Channel open
2021-02-08 10:47:36,869 DEBUG pub send {'test_me_send': 83} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2021-02-08 10:47:36,880 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 83}, <Message object at 0x110313050 with details {'body_length': 20, 'delivery_info': {'routing_key': u'r-pub', 'exchange': u'e-pub'}, 'properties': {}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 1}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:36,881 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 83},), kwargs={}, context={'parent_call_id': None, 'call_id': '073a02db-c263-492c-83cc-4ebfefd4eb90'})
2021-02-08 10:47:36,892 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:36,897 DEBUG using channel_id: 1
2021-02-08 10:47:36,901 DEBUG Channel open
2021-02-08 10:47:36,901 DEBUG rpc publish {'args': ({'test_me_send': 83},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"073a02db-c263-492c-83cc-4ebfefd4eb90"', 'namekox-h-parent_call_id': 'null'}, 'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f', 'retry': True, 'expiration': 20, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_ping', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:36,907 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 83}], u'kwargs': {}}, <Message object at 0x110313180 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_ping', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 1}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:36,908 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 83}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"073a02db-c263-492c-83cc-4ebfefd4eb90"', 'namekox-h-parent_call_id': 'null'}, u'priority': 0, u'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '20000'}
2021-02-08 10:47:36,908 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 83}], kwargs={}, context={'parent_call_id': None, 'call_id': '073a02db-c263-492c-83cc-4ebfefd4eb90'})
2021-02-08 10:47:36,910 DEBUG rpc publish {'args': ({u'test_me_send': 83},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"6ec80c21-47db-4200-896f-8b3d242ec279"', 'namekox-h-parent_call_id': '"073a02db-c263-492c-83cc-4ebfefd4eb90"'}, 'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_pong', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:36,914 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 83}], u'kwargs': {}}, <Message object at 0x110313050 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_pong', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 1}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:36,914 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 83}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"6ec80c21-47db-4200-896f-8b3d242ec279"', 'namekox-h-parent_call_id': '"073a02db-c263-492c-83cc-4ebfefd4eb90"'}, u'priority': 0, u'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '5000'}
2021-02-08 10:47:36,915 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 83}], kwargs={}, context={'parent_call_id': '073a02db-c263-492c-83cc-4ebfefd4eb90', 'call_id': '6ec80c21-47db-4200-896f-8b3d242ec279'})
2021-02-08 10:47:36,931 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 10:47:36,936 DEBUG using channel_id: 1
2021-02-08 10:47:36,941 DEBUG Channel open
2021-02-08 10:47:36,942 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 83}}} with {'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:36,980 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 83}}}, <Message object at 0x110313050 with details {'body_length': 63, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 1}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:36,981 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 83}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': '35a1033d-534b-4d1c-897f-ddc60a59324f', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '5000'}
2021-02-08 10:47:36,982 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 83}}}} with {'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f', 'retry': True, 'expiration': 20, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:36,987 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 83}}}}, <Message object at 0x110313180 with details {'body_length': 82, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 2}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:36,988 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 83}}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': '90a4c51d-6d55-4c18-901e-95e07a92938f', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '20000'}
2021-02-08 10:47:37,840 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2021-02-08 10:47:37,841 DEBUG pub send {'test_me_send': 70} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2021-02-08 10:47:37,842 DEBUG rpc publish {'args': ({'test_me_send': 70},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"d99e5694-9951-490b-acee-034bfc799f6b"', 'namekox-h-parent_call_id': 'null'}, 'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_ping', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:37,849 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 70}, <Message object at 0x110313050 with details {'body_length': 20, 'delivery_info': {'routing_key': u'r-pub', 'exchange': u'e-pub'}, 'properties': {}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 2}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:37,849 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 70}], u'kwargs': {}}, <Message object at 0x110313180 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_ping', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 2}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:37,849 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 70},), kwargs={}, context={'parent_call_id': None, 'call_id': 'd99e5694-9951-490b-acee-034bfc799f6b'})
2021-02-08 10:47:37,850 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 70}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"d99e5694-9951-490b-acee-034bfc799f6b"', 'namekox-h-parent_call_id': 'null'}, u'priority': 0, u'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '5000'}
2021-02-08 10:47:37,850 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 70}], kwargs={}, context={'parent_call_id': None, 'call_id': 'd99e5694-9951-490b-acee-034bfc799f6b'})
2021-02-08 10:47:37,851 DEBUG rpc publish {'args': ({u'test_me_send': 70},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"b2b8bb84-5dad-430b-af90-5056187eab9d"', 'namekox-h-parent_call_id': '"d99e5694-9951-490b-acee-034bfc799f6b"'}, 'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_pong', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:37,857 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 70}], u'kwargs': {}}, <Message object at 0x110313050 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_pong', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 2}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:37,858 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 70}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"b2b8bb84-5dad-430b-af90-5056187eab9d"', 'namekox-h-parent_call_id': '"d99e5694-9951-490b-acee-034bfc799f6b"'}, u'priority': 0, u'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '5000'}
2021-02-08 10:47:37,858 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 70}], kwargs={}, context={'parent_call_id': 'd99e5694-9951-490b-acee-034bfc799f6b', 'call_id': 'b2b8bb84-5dad-430b-af90-5056187eab9d'})
2021-02-08 10:47:37,859 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 70}}} with {'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:37,868 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 70}}}, <Message object at 0x110313050 with details {'body_length': 63, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 3}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:37,871 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 70}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': '5d9bb752-1cf6-4ab2-92e5-0d8239dbefc9', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '5000'}
2021-02-08 10:47:37,875 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 70}}}} with {'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:37,878 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 70}}}}, <Message object at 0x110313180 with details {'body_length': 82, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 4}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:37,879 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 70}}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': '9e07adfd-6272-432d-bf02-bd8e43f1c65b', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '5000'}
2021-02-08 10:47:38,836 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2021-02-08 10:47:38,838 DEBUG pub send {'test_me_send': 31} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2021-02-08 10:47:38,839 DEBUG rpc publish {'args': ({'test_me_send': 31},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"2129bce2-51c2-45f1-949c-955c13b49d9b"', 'namekox-h-parent_call_id': 'null'}, 'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_ping', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:38,843 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 31}], u'kwargs': {}}, <Message object at 0x110313050 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_ping', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 3}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:38,844 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 31}, <Message object at 0x110313180 with details {'body_length': 20, 'delivery_info': {'routing_key': u'r-pub', 'exchange': u'e-pub'}, 'properties': {}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 3}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:38,844 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 31}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"2129bce2-51c2-45f1-949c-955c13b49d9b"', 'namekox-h-parent_call_id': 'null'}, u'priority': 0, u'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '5000'}
2021-02-08 10:47:38,845 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 31}], kwargs={}, context={'parent_call_id': None, 'call_id': '2129bce2-51c2-45f1-949c-955c13b49d9b'})
2021-02-08 10:47:38,845 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 31},), kwargs={}, context={'parent_call_id': None, 'call_id': '2129bce2-51c2-45f1-949c-955c13b49d9b'})
2021-02-08 10:47:38,846 DEBUG rpc publish {'args': ({u'test_me_send': 31},), 'kwargs': {}} with {'headers': {'namekox-h-call_id': '"e370cf52-a7e1-4f52-b611-507a59b71cb7"', 'namekox-h-parent_call_id': '"2129bce2-51c2-45f1-949c-955c13b49d9b"'}, 'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-e-ping(topic)>, 'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'routing_key': 'namekox-r-ping-rpc_pong', 'serializer': 'json', 'retry_policy': {'max_retries': 3}}
2021-02-08 10:47:38,851 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 31}], u'kwargs': {}}, <Message object at 0x110313180 with details {'body_length': 46, 'delivery_info': {'routing_key': u'namekox-r-ping-rpc_pong', 'exchange': u'namekox-e-ping'}, 'properties': {'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 3}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:38,851 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 31}], u'kwargs': {}} with {u'delivery_mode': 2, u'application_headers': {'namekox-h-call_id': '"e370cf52-a7e1-4f52-b611-507a59b71cb7"', 'namekox-h-parent_call_id': '"2129bce2-51c2-45f1-949c-955c13b49d9b"'}, u'priority': 0, u'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'reply_to': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', u'expiration': '5000'}
2021-02-08 10:47:38,851 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 31}], kwargs={}, context={'parent_call_id': '2129bce2-51c2-45f1-949c-955c13b49d9b', 'call_id': 'e370cf52-a7e1-4f52-b611-507a59b71cb7'})
2021-02-08 10:47:38,852 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 31}}} with {'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:38,855 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 31}}}, <Message object at 0x110313180 with details {'body_length': 63, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 5}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:38,856 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 31}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': '808f1b37-3626-4bce-8eb4-e010a8601e70', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '5000'}
2021-02-08 10:47:38,857 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 31}}}} with {'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a', 'retry': True, 'expiration': 5, 'exchange': <unbound Exchange namekox-re-global(topic)>, 'routing_key': 'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'serializer': 'json', 'retry_policy': {'max_retries': 3}} succ
2021-02-08 10:47:38,860 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 31}}}}, <Message object at 0x110313050 with details {'body_length': 82, 'delivery_info': {'routing_key': u'namekox-rr-ping-listener.d3d188e0-c004-40e5-8a29-b1563bd15070', 'exchange': u'namekox-re-global'}, 'properties': {'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a'}, 'state': u'RECEIVED', 'content_type': 'application/json', 'delivery_tag': 6}>), kwargs={}, tid=handle_message)
2021-02-08 10:47:38,860 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 31}}}} with {u'delivery_mode': 2, u'application_headers': {}, u'priority': 0, u'correlation_id': 'b55fa91f-bc44-4e90-9e24-142b57f8f56a', u'content_encoding': 'utf-8', u'content_type': 'application/json', u'expiration': '5000'}
^C2021-02-08 10:47:39,279 DEBUG stopping services ['ping']
2021-02-08 10:47:39,279 DEBUG stopping service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer]
2021-02-08 10:47:39,281 DEBUG wait service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer] stop
2021-02-08 10:47:39,282 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer] stopped
2021-02-08 10:47:39,282 DEBUG stopping service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc]
2021-02-08 10:47:39,284 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc] stopped
2021-02-08 10:47:39,288 DEBUG services ['ping'] stopped
2021-02-08 10:47:39,289 DEBUG killing services ['ping']
2021-02-08 10:47:39,294 DEBUG service ping already stopped
2021-02-08 10:47:39,295 DEBUG services ['ping'] killed
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
    RABBITMQ_USER = 'admin'
    RABBITMQ_PASS = 'nimda'
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = 5672
    RABBITMQ_PATH = '/'

    uri = 'pyamqp://{}:{}@{}:{}/{}'.format(
        RABBITMQ_USER,
        RABBITMQ_PASS,
        RABBITMQ_HOST,
        RABBITMQ_PORT,
        RABBITMQ_PATH)
    config = {'AMQP': {'rpc': {'timeout': 20}, 'uri': uri}}
    t = time.time()
    n = random.randint(1, 100)
    p = RpcStandaloneProxy(config).get_instance()
    r = p(timeout=1).ping.rpc_ping(n)
    print('Got cluster rpc result: {}, cost: {}s'.format(r, time.time()-t))
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_amqp.cli.subctx.amqprpc:AMQPRpcProxy
  - namekox_amqp.cli.subctx.amqppub:AMQPPubProxy
AMQP:
  qos: 50
  uri: pyamqp://admin:nimda@127.0.0.1:5672//
```

> namekox shell
```shell script
Namekox Python 2.7.16 (default, Jun  5 2020, 22:59:21)
[GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc- shell on darwin
In [1]: nx.amqprpc.proxy.ping.rpc_ping('nb')
2021-02-08 11:05:20,763 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 11:05:20,781 DEBUG using channel_id: 1
2021-02-08 11:05:20,787 DEBUG Channel open
2021-02-08 11:05:20,854 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 11:05:20,859 DEBUG using channel_id: 1
2021-02-08 11:05:20,862 DEBUG Channel open
2021-02-08 11:05:20,944 DEBUG Closed channel #1
Out[1]: {u'rpc_ping_recv': {u'rpc_pong_recv': u'nb'}}

In [2]: from kombu import Exchange

In [3]: nx.amqppub.proxy(Exchange('e-pub', 'topic'), routing_key='r-pub').send_async({'nb': True})
2021-02-08 11:05:41,051 DEBUG Start from server, version: 0.9, properties: {'information': 'Licensed under the MPL 1.1. Website: https://rabbitmq.com', 'product': 'RabbitMQ', 'copyright': 'Copyright (c) 2007-2019 Pivotal Software, Inc.', 'capabilities': {'exchange_exchange_bindings': True, 'connection.blocked': True, 'authentication_failure_close': True, 'direct_reply_to': True, 'basic.nack': True, 'per_consumer_qos': True, 'consumer_priorities': True, 'consumer_cancel_notify': True, 'publisher_confirms': True}, 'cluster_name': 'rabbit@a0b3d1669709', 'platform': 'Erlang/OTP 22.1.7', 'version': '3.8.1'}, mechanisms: ['PLAIN', 'AMQPLAIN'], locales: [u'en_US']
2021-02-08 11:05:41,055 DEBUG using channel_id: 1
2021-02-08 11:05:41,063 DEBUG Channel open
2021-02-08 11:05:41,065 DEBUG cluster.pub send {'nb': True} with {'serializer': 'json', 'retry': True, 'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>, 'retry_policy': {'max_retries': 3}} succ
```
