#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from eventlet.event import Event
from kombu.mixins import ConsumerMixin
from namekox_core.core.friendly import ignore_exception
from namekox_core.core.service.extension import ControlExtension


from .connection import AMQPConnect


logger = getLogger(__name__)


class BaseAMQPConsumer(ConsumerMixin, ControlExtension):
    def __init__(self, *args, **kwargs):
        self.gt = None
        self.started = False
        self.connection = None
        self.consumers_ready = Event()
        self.consumers_channels = set()
        super(BaseAMQPConsumer, self).__init__(*args, **kwargs)

    # Extension
    def _link_manage_results(self, gt):
        def exc_func(exc_info):
            exc_type, exc_value, exc_trace = exc_info
            self.consumers_ready.send_exception(exc_value)
        ignore_exception(gt.wait, exc_func=exc_func)()

    def setup(self):
        self.connection = AMQPConnect(self.container.config).instance

    def start(self):
        if self.started:
            return
        self.started = True
        self.gt = self.container.spawn_manage_thread(self.run)
        self.gt.link(self._link_manage_results)
        try:
            self.consumers_ready.wait()
        except Exception as e:
            msg = 'amqp consumers failed to start, {}'.format(e.message)
            logger.error(msg)
        else:
            msg = 'amqp consumers ready.'
            logger.debug(msg)
        return

    def stop(self):
        self.should_stop = True
        self.started = False
        self.gt.kill()

    def kill(self):
        self.should_stop = True
        self.started = False
        self.gt.kill()

    # ConsumerMixin
    def get_consumers(self, consumer_cls, channel):
        raise NotImplementedError

    def create_connection(self):
        return super(BaseAMQPConsumer, self).create_connection()

    def on_message(self, extension, body, message):
        self.container.spawn_manage_thread(extension.handle_message, args=(body, message))

    def on_connection_revived(self):
        return super(BaseAMQPConsumer, self).on_connection_revived()

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        not self.consumers_ready.ready() and self.consumers_ready.send(None)
        return super(BaseAMQPConsumer, self).on_consume_ready(connection, channel, consumers, **kwargs)

    def on_consume_end(self, connection, channel):
        return super(BaseAMQPConsumer, self).on_consume_end(connection, channel)

    def on_iteration(self):
        return super(BaseAMQPConsumer, self).on_iteration()

    def on_decode_error(self, message, exc):
        return super(BaseAMQPConsumer, self).on_decode_error(message, exc)

    def on_connection_error(self, exc, interval):
        return super(BaseAMQPConsumer, self).on_connection_error(exc, interval)
