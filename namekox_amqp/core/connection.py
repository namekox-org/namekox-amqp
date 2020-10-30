#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu import Connection, pools
from kombu.pools import connections
from namekox_amqp.constants import (
    AMQP_CONFIG_KEY,
    DEFAULT_AMQP_URI,
    DEFAULT_AMQP_SSL,
    DEFAULT_AMQP_HEARTBEAT,
    DEFAULT_AMQP_TRANSPORT,
)
from namekox_core.core.friendly import as_singleton_cls, AsLazyProperty


pool = pools.Connections(limit=4)


@as_singleton_cls
class AMQPConnect(object):
    def __init__(self, config):
        self.config = config
        self.curobj = Connection(self.amqp_uri, **self.conn_cfg)

    @AsLazyProperty
    def amqp_uri(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        return config.get('uri', DEFAULT_AMQP_URI) or DEFAULT_AMQP_URI

    @AsLazyProperty
    def conn_cfg(self):
        config = self.config.get(AMQP_CONFIG_KEY, {}) or {}
        ssloption = config.get('ssl', DEFAULT_AMQP_SSL)
        heartbeat = config.get('heartbeat', DEFAULT_AMQP_HEARTBEAT)
        transport = config.get('transport', DEFAULT_AMQP_TRANSPORT)
        return {'transport_options': transport, 'heartbeat': heartbeat, 'ssl': ssloption}
