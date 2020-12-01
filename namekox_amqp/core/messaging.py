#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import six
import anyjson


from namekox_amqp.constants import (
    DEFAULT_AMQP_H_PREFIX,
    DEFAULT_AMQP_E_PREFIX,
    DEFAULT_AMQP_R_PREFIX,
    DEFAULT_AMQP_Q_PREFIX,
    DEFAULT_AMQP_RE_PREFIX,
    DEFAULT_AMQP_RR_PREFIX,
    DEFAULT_AMQP_RQ_PREFIX,
)


def gen_message_headers(context):
    headers = {}
    for k, v in six.iteritems(context):
        k = '{}-'.format(DEFAULT_AMQP_H_PREFIX) + k
        headers.update({k: anyjson.serialize(v)})
    return headers


def get_message_headers(message):
    headers = {}
    for k, v in six.iteritems(message.headers):
        p = '{}-'.format(DEFAULT_AMQP_H_PREFIX)
        k.startswith(p) and headers.update({k[len(p):]: anyjson.deserialize(v)})
    return headers


def get_reply_exchange_name():
    return DEFAULT_AMQP_RE_PREFIX


def get_exchange_name(service_name):
    return '{}-{}'.format(DEFAULT_AMQP_E_PREFIX, service_name)


def get_queue_name(service_name, obj_name):
    return '{}-{}-{}'.format(DEFAULT_AMQP_Q_PREFIX, service_name, obj_name)


def get_route_name(service_name, obj_name):
    return '{}-{}-{}'.format(DEFAULT_AMQP_R_PREFIX, service_name, obj_name)


def get_reply_queue_name(service_name, obj_name, random_id):
    return '{}-{}-{}.{}'.format(DEFAULT_AMQP_RQ_PREFIX, service_name, obj_name, random_id)


def get_reply_route_name(service_name, obj_name, random_id):
    return '{}-{}-{}.{}'.format(DEFAULT_AMQP_RR_PREFIX, service_name, obj_name, random_id)
