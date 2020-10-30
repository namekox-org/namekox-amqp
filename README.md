# Install
```shell script
bash install.sh
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
  uri: pyamqp://admin:**@127.0.0.1:5672//
  transport: ~
  heartbeat: 15
  serializer: json
```

> namekox run ping
```shell script
2020-10-30 11:53:25,973 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-10-30 11:53:25,980 DEBUG starting services ['ping']
2020-10-30 11:53:25,981 DEBUG starting service ping entrypoints [ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer]
2020-10-30 11:53:25,981 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-10-30 11:53:25,981 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-10-30 11:53:25,982 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-10-30 11:53:26,002 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-10-30 11:53:26,002 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-10-30 11:53:26,006 DEBUG Open OK!
2020-10-30 11:53:26,007 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-10-30 11:53:26,007 DEBUG using channel_id: 1
2020-10-30 11:53:26,009 DEBUG Open OK!
2020-10-30 11:53:26,009 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-10-30 11:53:26,010 DEBUG using channel_id: 1
2020-10-30 11:53:26,016 DEBUG Channel open
2020-10-30 11:53:26,016 DEBUG rpc_ping -LISTEN-> namekox-q-ping-rpc_ping -BIND-> namekox-e-ping
2020-10-30 11:53:26,016 DEBUG using channel_id: 2
2020-10-30 11:53:26,017 DEBUG Channel open
2020-10-30 11:53:26,017 DEBUG amq_sub -LISTEN-> namekox-q-ping-amq_sub -BIND-> e-pub
2020-10-30 11:53:26,018 DEBUG using channel_id: 2
2020-10-30 11:53:26,024 DEBUG Channel open
2020-10-30 11:53:26,024 DEBUG Channel open
2020-10-30 11:53:26,042 DEBUG rpc_pong -LISTEN-> namekox-q-ping-rpc_pong -BIND-> namekox-e-ping
2020-10-30 11:53:26,042 DEBUG using channel_id: 3
2020-10-30 11:53:26,043 DEBUG amqp consumers ready.
2020-10-30 11:53:26,047 DEBUG Channel open
2020-10-30 11:53:26,066 DEBUG amqp consumers ready.
2020-10-30 11:53:26,066 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer] started
2020-10-30 11:53:26,066 DEBUG starting service ping dependencies [ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener]
2020-10-30 11:53:26,067 DEBUG spawn manage thread handle ping:kombu.mixins:run(args=(), kwargs={}, tid=run)
2020-10-30 11:53:26,081 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-10-30 11:53:26,086 DEBUG Open OK!
2020-10-30 11:53:26,087 INFO Connected to amqp://admin:**@127.0.0.1:5672//
2020-10-30 11:53:26,087 DEBUG using channel_id: 1
2020-10-30 11:53:26,091 DEBUG Channel open
2020-10-30 11:53:26,091 DEBUG listener -LISTEN-> namekox-rq-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd -BIND-> namekox-re-global
2020-10-30 11:53:26,091 DEBUG using channel_id: 2
2020-10-30 11:53:26,095 DEBUG Channel open
2020-10-30 11:53:26,122 DEBUG amqp consumers ready.
2020-10-30 11:53:26,122 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener] started
2020-10-30 11:53:26,122 DEBUG services ['ping'] started
2020-10-30 11:53:26,987 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2020-10-30 11:53:27,008 DEBUG Start from server, version: 0.9, properties: {u'information': u'Licensed under the MPL 1.1. Website: https://rabbitmq.com', u'product': u'RabbitMQ', u'copyright': u'Copyright (c) 2007-2019 Pivotal Software, Inc.', u'capabilities': {u'exchange_exchange_bindings': True, u'connection.blocked': True, u'authentication_failure_close': True, u'direct_reply_to': True, u'basic.nack': True, u'per_consumer_qos': True, u'consumer_priorities': True, u'consumer_cancel_notify': True, u'publisher_confirms': True}, u'cluster_name': u'rabbit@a0b3d1669709', u'platform': u'Erlang/OTP 22.1.7', u'version': u'3.8.1'}, mechanisms: [u'PLAIN', u'AMQPLAIN'], locales: [u'en_US']
2020-10-30 11:53:27,016 DEBUG Open OK!
2020-10-30 11:53:27,016 DEBUG using channel_id: 1
2020-10-30 11:53:27,019 DEBUG Channel open
2020-10-30 11:53:27,019 DEBUG pub send {'test_me_send': 21} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2020-10-30 11:53:27,020 DEBUG rpc publish {'args': ({'test_me_send': 21},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_ping', 'headers': {}, 'correlation_id': 'f3b546a9-224d-4dd3-9e3c-4812c2184a89', 'expiration': 20, 'reply_to': 'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json'} succ
2020-10-30 11:53:27,023 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 21}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,023 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 21},), kwargs={}, context={})
2020-10-30 11:53:27,023 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 21}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10dccb6d8>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,024 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 21}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'f3b546a9-224d-4dd3-9e3c-4812c2184a89', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'expiration': u'20000'}
2020-10-30 11:53:27,024 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 21}], kwargs={}, context={})
2020-10-30 11:53:27,025 DEBUG rpc publish {'args': ({u'test_me_send': 21},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_pong', 'headers': {}, 'correlation_id': 'f7b59b7d-71f0-41d9-9fbb-f5a40d1b73cb', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json'} succ
2020-10-30 11:53:27,030 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 21}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,030 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 21}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'f7b59b7d-71f0-41d9-9fbb-f5a40d1b73cb', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'expiration': u'5000'}
2020-10-30 11:53:27,031 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 21}], kwargs={}, context={})
2020-10-30 11:53:27,031 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 21}}} with {'correlation_id': u'f7b59b7d-71f0-41d9-9fbb-f5a40d1b73cb', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-10-30 11:53:27,067 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 21}}}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,068 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 21}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'f7b59b7d-71f0-41d9-9fbb-f5a40d1b73cb', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
2020-10-30 11:53:27,068 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 21}}}} with {'correlation_id': u'f3b546a9-224d-4dd3-9e3c-4812c2184a89', 'expiration': 20, 'routing_key': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-10-30 11:53:27,071 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 21}}}}, <kombu.transport.pyamqp.Message object at 0x10dccb6d8>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,072 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 21}}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'f3b546a9-224d-4dd3-9e3c-4812c2184a89', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'20000'}
2020-10-30 11:53:27,984 DEBUG spawn worker thread handle ping:test_me(args=(), kwargs={}, context=None)
2020-10-30 11:53:27,985 DEBUG pub send {'test_me_send': 11} with {'routing_key': 'r-pub', 'exchange': <unbound Exchange e-pub(topic)>} succ
2020-10-30 11:53:27,986 DEBUG rpc publish {'args': ({'test_me_send': 11},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_ping', 'headers': {}, 'correlation_id': 'cf0c0231-785a-40b0-943b-81a44c445b7e', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json'} succ
2020-10-30 11:53:27,990 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 11}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10dccb6d8>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,990 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.sub.handler:handle_message(args=({u'test_me_send': 11}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,991 DEBUG rpc_ping receive {u'args': [{u'test_me_send': 11}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'cf0c0231-785a-40b0-943b-81a44c445b7e', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'expiration': u'5000'}
2020-10-30 11:53:27,991 DEBUG spawn worker thread handle ping:rpc_ping(args=[{u'test_me_send': 11}], kwargs={}, context={})
2020-10-30 11:53:27,991 DEBUG spawn worker thread handle ping:amq_sub(args=({u'test_me_send': 11},), kwargs={}, context={})
2020-10-30 11:53:27,992 DEBUG rpc publish {'args': ({u'test_me_send': 11},), 'kwargs': {}} with {'exchange': <unbound Exchange namekox-e-ping(topic)>, 'routing_key': 'namekox-r-ping-rpc_pong', 'headers': {}, 'correlation_id': 'fcd27980-66ae-4799-97cd-5d71738b60ff', 'expiration': 5, 'reply_to': 'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json'} succ
2020-10-30 11:53:27,999 DEBUG spawn manage thread handle ping:namekox_amqp.core.entrypoints.rpc.handler:handle_message(args=({u'args': [{u'test_me_send': 11}], u'kwargs': {}}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:27,999 DEBUG rpc_pong receive {u'args': [{u'test_me_send': 11}], u'kwargs': {}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'fcd27980-66ae-4799-97cd-5d71738b60ff', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'reply_to': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'expiration': u'5000'}
2020-10-30 11:53:27,999 DEBUG spawn worker thread handle ping:rpc_pong(args=[{u'test_me_send': 11}], kwargs={}, context={})
2020-10-30 11:53:28,001 DEBUG rpc_pong publish {'errs': None, 'data': {'rpc_pong_recv': {u'test_me_send': 11}}} with {'correlation_id': u'fcd27980-66ae-4799-97cd-5d71738b60ff', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-10-30 11:53:28,005 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 11}}}, <kombu.transport.pyamqp.Message object at 0x10dccb640>), kwargs={}, tid=handle_message)
2020-10-30 11:53:28,005 DEBUG listener receive {u'errs': None, u'data': {u'rpc_pong_recv': {u'test_me_send': 11}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'fcd27980-66ae-4799-97cd-5d71738b60ff', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
2020-10-30 11:53:28,006 DEBUG rpc_ping publish {'errs': None, 'data': {'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 11}}}} with {'correlation_id': u'cf0c0231-785a-40b0-943b-81a44c445b7e', 'expiration': 5, 'routing_key': u'namekox-rr-ping-listener.64cfb2eb-4471-4607-b6bc-7f800b0360cd', 'serializer': 'json', 'exchange': <unbound Exchange namekox-re-global(topic)>} succ
2020-10-30 11:53:28,014 DEBUG spawn manage thread handle ping:namekox_amqp.core.dependencies.rpc.listener:handle_message(args=({u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 11}}}}, <kombu.transport.pyamqp.Message object at 0x10dccb6d8>), kwargs={}, tid=handle_message)
2020-10-30 11:53:28,014 DEBUG listener receive {u'errs': None, u'data': {u'rpc_ping_recv': {u'rpc_pong_recv': {u'test_me_send': 11}}}} with {'delivery_mode': 2, 'application_headers': {}, 'priority': 0, 'correlation_id': u'cf0c0231-785a-40b0-943b-81a44c445b7e', 'content_encoding': u'utf-8', 'content_type': u'application/json', 'expiration': u'5000'}
^C2020-10-30 11:53:28,599 DEBUG stopping services ['ping']
2020-10-30 11:53:28,599 DEBUG stopping service ping entrypoints [ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer]
2020-10-30 11:53:28,600 DEBUG wait service ping entrypoints [ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer] stop
2020-10-30 11:53:28,600 DEBUG service ping entrypoints [ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_ping, ping:namekox_timer.core.entrypoints.timer.Timer:test_me, ping:namekox_amqp.core.entrypoints.sub.consumer.AMQPSubConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.handler.AMQPRpcHandler:rpc_pong, ping:namekox_amqp.core.entrypoints.sub.handler.AMQPSubHandler:amq_sub, ping:namekox_amqp.core.entrypoints.rpc.consumer.AMQPRpcConsumer:consumer, ping:namekox_amqp.core.entrypoints.rpc.producer.AMQPRpcProducer:producer] stopped
2020-10-30 11:53:28,600 DEBUG stopping service ping dependencies [ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener]
2020-10-30 11:53:28,600 DEBUG service ping dependencies [ping:namekox_amqp.core.dependencies.rpc.AMQPRpcProxy:rpc, ping:namekox_amqp.core.dependencies.rpc.consumer.AMQPReplyConsumer:consumer, ping:namekox_amqp.core.dependencies.pub.AMQPPubProxy:pub, ping:namekox_amqp.core.dependencies.rpc.listener.AMQPRpcListener:listener] stopped
2020-10-30 11:53:28,602 DEBUG services ['ping'] stopped
2020-10-30 11:53:28,603 DEBUG killing services ['ping']
2020-10-30 11:53:28,603 DEBUG service ping already stopped
2020-10-30 11:53:28,604 DEBUG services ['ping'] killed
```
