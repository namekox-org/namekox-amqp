#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from namekox_core.core.friendly import as_wraps_partial
from namekox_core.core.service.entrypoint import Entrypoint
from namekox_amqp.core.messaging import get_message_headers


from .response import RpcResponse
from .consumer import AMQPRpcConsumer
from .producer import AMQPRpcProducer


logger = getLogger(__name__)


class AMQPRpcHandler(Entrypoint):
    consumer = AMQPRpcConsumer()
    producer = AMQPRpcProducer()

    def __init__(self, **reply_options):
        self.reply_options = reply_options
        super(AMQPRpcHandler, self).__init__(**reply_options)

    def setup(self):
        self.consumer.register_extension(self)

    def stop(self):
        self.consumer.unregister_extension(self)
        self.consumer.wait_extension_stop()

    def rsp_handler(self, message, context, result, exc_info):
        response = RpcResponse(self, message)
        result, exc_info = response.reply(result, exc_info)
        message.ack()
        return result, exc_info

    def res_handler(self, message, context, result, exc_info):
        response = RpcResponse(self, message)
        result, exc_info = response.reply(result, exc_info)
        message.ack()
        return result, exc_info

    @staticmethod
    def _check_message(body):
        return isinstance(body, dict) and 'args' in body and 'kwargs' in body

    def handle_message(self, body, message):
        logger.debug('{} receive {} with {}'.format(self.obj_name, body, message.properties))
        if not self._check_message(body):
            msg = '{} not dict? missing `args`? missing `kwargs`?'
        elif not message.properties.get('reply_to', None):
            msg = '{} missing `reply_to` in message.properties?'
        elif not message.properties.get('correlation_id', None):
            msg = '{} missing `correlation_id` in message.properties?'
        else:
            msg = ''
        msg = msg.format(body)
        msg and logger.warn(msg)
        msg and message.ack()
        args, kwargs = body['args'], body['kwargs']
        ctxdata = get_message_headers(message)
        res_handler = as_wraps_partial(self.res_handler, message)
        msg or self.container.spawn_worker_thread(self, args, kwargs, ctx_data=ctxdata, res_handler=res_handler)
