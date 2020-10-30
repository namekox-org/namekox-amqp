#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import sys
import kombu.exceptions
import kombu.serialization


from logging import getLogger
from kombu.pools import producers
from namekox_amqp.exceptions import SerializeError
from namekox_core.exceptions import gen_exc_to_data


logger = getLogger(__name__)


class RpcResponse(object):
    def __init__(self, entrypoint, message):
        self.message = message
        self.entrypoint = entrypoint

    @property
    def exchange(self):
        return self.entrypoint.producer.exchange

    @property
    def connection(self):
        return self.entrypoint.producer.connection

    @property
    def serializer(self):
        return self.entrypoint.producer.serializer

    @property
    def routekey(self):
        return self.message.properties['reply_to']

    @property
    def correlation_id(self):
        return self.message.properties['correlation_id']

    @property
    def expiration(self):
        timeout = self.message.properties.get('expiration', None)
        return timeout if timeout is None else int(int(timeout)/1000)

    def reply(self, result, exc_info):
        errs = None
        if exc_info is not None:
            exc_type, exc_value, exc_trace = exc_info
            errs = gen_exc_to_data(exc_value)
        try:
            kombu.serialization.dumps(result, self.serializer)
        except kombu.exceptions.SerializationError:
            exc_info = sys.exc_info()
            exc_value = SerializeError(result)
            errs = gen_exc_to_data(exc_value)
            result = None
        resp = {'data': result, 'errs': errs}
        reply_options = self.entrypoint.reply_options.copy()
        reply_options.update({
            'exchange': self.exchange,
            'routing_key': self.routekey,
            'serializer': self.serializer,
            'correlation_id': self.correlation_id
        })
        reply_options.setdefault('expiration', self.expiration)
        with producers[self.connection].acquire(block=False) as producer:
            producer.publish(resp, **reply_options)
        msg = '{} publish {} with {} succ'.format(self.entrypoint.obj_name, resp, reply_options)
        logger.debug(msg)
        return result, exc_info
