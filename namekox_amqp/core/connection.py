#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_amqp.constants import (
    AMQP_CONFIG_KEY,
    DEFAULT_AMQP_URI,
    DEFAULT_AMQP_SSL,
    DEFAULT_AMQP_HEARTBEAT,
    DEFAULT_AMQP_TRANSPORT_OPTIONS,
)
from kombu import Connection as BaseConnection
from namekox_core.core.friendly import AsLazyProperty


from .producer import Producer


class Connection(BaseConnection):
    def Producer(self, channel=None, *args, **kwargs):
        return Producer(channel or self, *args, **kwargs)


class AMQPConnect(object):
    def __init__(self, config):
        self.config = config

    @AsLazyProperty
    def instance(self):
        return Connection(self.amqp_uri, **self.conn_cfg)

    @AsLazyProperty
    def amqp_uri(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('uri', DEFAULT_AMQP_URI) or DEFAULT_AMQP_URI

    @AsLazyProperty
    def conn_cfg(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        ssl = config.get('ssl', DEFAULT_AMQP_SSL)
        heartbeat = config.get('heartbeat', DEFAULT_AMQP_HEARTBEAT)
        transport_options = DEFAULT_AMQP_TRANSPORT_OPTIONS.copy()
        transport_options.update(config.get('transport_options', {}))
        config = config.copy()
        config.update({'ssl': ssl,
                       'heartbeat': heartbeat,
                       'transport_options': transport_options
                       })
        return config
