#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sys
import kombu.exceptions
import kombu.serialization


from logging import getLogger
from namekox_amqp.exceptions import SerializeError
from namekox_core.exceptions import gen_exc_to_data
from namekox_amqp.constants import DEFAULT_AMQP_PUBLISHER_OPTIONS


logger = getLogger(__name__)


class RpcResponse(object):
    def __init__(self, ext, msg):
        self.msg = msg
        self.ext = ext

    @property
    def connect(self):
        return self.ext.producer.connect

    @property
    def exchange(self):
        return self.ext.producer.exchange

    @property
    def producer(self):
        return self.ext.producer.producer

    @property
    def serializer(self):
        return self.ext.producer.serializer

    @property
    def routekey(self):
        return self.msg.properties['reply_to']

    @property
    def correlation_id(self):
        return self.msg.properties['correlation_id']

    @property
    def expiration(self):
        timeout = self.msg.properties.get('expiration', None)
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
        reply_options = DEFAULT_AMQP_PUBLISHER_OPTIONS.copy()
        reply_options.update(self.ext.reply_options)
        reply_options.update({
            'exchange': self.exchange,
            'routing_key': self.routekey,
            'serializer': self.serializer,
            'correlation_id': self.correlation_id
        })
        reply_options.setdefault('expiration', self.expiration)
        self.producer.publish(resp, **reply_options)
        msg = '{} publish {} with {} succ'.format(
            self.ext.obj_name, resp, reply_options
        )
        logger.debug(msg)
        return result, exc_info
