#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from logging import getLogger
from namekox_amqp.exceptions import RpcTimeout
from namekox_core.exceptions import gen_exc_to_data, gen_data_to_exc


logger = getLogger(__name__)


class RpcReplyProxy(object):
    def __init__(self, reply_event):
        self.reply_event = reply_event

    @staticmethod
    def raise_again(errs):
        raise gen_data_to_exc(errs)

    def result(self):
        timeout = self.reply_event.timeout
        errs = gen_exc_to_data(RpcTimeout(timeout))
        resp = self.reply_event.r_event.wait(timeout)
        resp is None and self.raise_again(errs)
        errs = resp['errs']
        errs and self.raise_again(errs)
        return resp['data']
