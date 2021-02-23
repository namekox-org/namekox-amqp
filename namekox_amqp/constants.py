#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


AMQP_CONFIG_KEY = 'AMQP'
DEFAULT_AMQP_QOS = 50
DEFAULT_AMQP_SSL = None
DEFAULT_AMQP_TRANSPORT_OPTIONS = {
    'interval_max': 30,
    'interval_start': 2,
    'interval_step': 2,
}
DEFAULT_AMQP_PUBLISHER_OPTIONS = {
    'retry': True,
    'retry_policy': {'max_retries': 3},
}
DEFAULT_AMQP_HEARTBEAT = 60
DEFAULT_AMQP_RPC_TIMEOUT = 20
DEFAULT_AMQP_SERIALIZE = 'json'
DEFAULT_AMQP_Q_PREFIX = 'namekox-q'
DEFAULT_AMQP_R_PREFIX = 'namekox-r'
DEFAULT_AMQP_E_PREFIX = 'namekox-e'
DEFAULT_AMQP_H_PREFIX = 'namekox-h'
DEFAULT_AMQP_RR_PREFIX = 'namekox-rr'
DEFAULT_AMQP_RQ_PREFIX = 'namekox-rq'
DEFAULT_AMQP_RE_PREFIX = 'namekox-re-global'
DEFAULT_AMQP_URI = 'pyamqp://guest:guest@localhost:5672//'
