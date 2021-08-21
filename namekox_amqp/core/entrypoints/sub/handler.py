#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

from logging import getLogger
from namekox_core.core.friendly import as_wraps_partial
from namekox_amqp.core.messaging import get_message_headers
from namekox_core.core.service.entrypoint import Entrypoint

from .consumer import AMQPSubConsumer

logger = getLogger(__name__)


class AMQPSubHandler(Entrypoint):
    consumer = AMQPSubConsumer()

    def __init__(self, exchange, **queue_options):
        self.exchange = exchange
        queue_options['exchange'] = exchange
        self.queue_options = queue_options
        super(AMQPSubHandler, self).__init__(exchange, **queue_options)

    def setup(self):
        self.consumer.register_extension(self)

    def stop(self):
        self.consumer.unregister_extension(self)
        self.consumer.wait_extension_stop()

    def res_handler(self, message, context, result, exc_info):
        message.ack()
        return result, exc_info

    def handle_message(self, body, message):
        args, kwargs = (body,), {}
        ctxdata = get_message_headers(message)
        res_handler = as_wraps_partial(self.res_handler, message)
        try:
            self.container.spawn_worker_thread(self, args, kwargs, ctx_data=ctxdata, res_handler=res_handler).wait()
        except:
            logger.error('unexpected error while consumer consume', exc_info=True)
