#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from namekox_amqp.exceptions import RpcTimeout
from namekox_core.exceptions import gen_exc_to_data, gen_data_to_exc


logger = getLogger(__name__)


class RpcReplyProxy(object):
    def __init__(self, event):
        self.event = event

    @staticmethod
    def raise_again(errs):
        raise gen_data_to_exc(errs)

    def result(self):
        timeout = self.event.timeout
        errs = gen_exc_to_data(RpcTimeout(timeout))
        resp = self.event.gtevent.wait(timeout)
        resp is None and self.raise_again(errs)
        errs = resp['errs']
        errs and self.raise_again(errs)
        return resp['data']
