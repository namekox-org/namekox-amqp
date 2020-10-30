#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import time


from eventlet import Event
from logging import getLogger
from amqp.exceptions import AMQPError
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.extension import SharedExtension
from namekox_core.core.service.dependency import DependencyProvider
from namekox_amqp.constants import AMQP_CONFIG_KEY, DEFAULT_AMQP_QOS


from .consumer import AMQPReplyConsumer


logger = getLogger(__name__)


class ReplyEvent(object):
    def __init__(self, r_event, timeout=None):
        self.r_event = r_event
        self.timeout = timeout
        self.curtime = time.time()

    @property
    def as_dict(self):
        return {'curtime': self.curtime, 'timeout': self.timeout}

    @property
    def expired(self):
        return self.curtime + self.timeout * 1000 >= time.time() if self.timeout is not None else False

    def __str__(self):
        return '{}'.format(self.as_dict)

    def __repr__(self):
        return '{}'.format(self.as_dict)


class AMQPRpcListener(SharedExtension, DependencyProvider):
    consumer = AMQPReplyConsumer()

    def __init__(self, *args, **kwargs):
        self.reply_events = {}
        super(AMQPRpcListener, self).__init__(*args, **kwargs)

    def setup(self):
        self.consumer.register_extension(self)

    def stop(self):
        self.consumer.unregister_extension(self)
        self.consumer.wait_extension_stop()

    @AsLazyProperty
    def maxqos(self):
        config = self.container.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('qos', DEFAULT_AMQP_QOS) or DEFAULT_AMQP_QOS

    def _cleanup_events(self):
        reply_events = {}
        for correlation_id in self.reply_events:
            re = self.reply_events['correlation_id']
            if re.expired:
                continue
            reply_events[correlation_id] = re
        return reply_events

    def get_reply_event(self, correlation_id, timeout=None):
        re = ReplyEvent(Event(), timeout=timeout)
        self.reply_events[correlation_id] = re
        return self.reply_events[correlation_id]

    def handle_message(self, body, message):
        try:
            message.ack()
        except AMQPError:
            return
        msg = '{} receive {} with {}'.format(self.obj_name, body, message.properties)
        logger.debug(msg)
        len(self.reply_events) >= self.maxqos and self._cleanup_events()
        correlation_id = message.properties.get('correlation_id', None)
        reply_event = self.reply_events.pop(correlation_id, None)
        reply_event and reply_event.r_event.send(body)

