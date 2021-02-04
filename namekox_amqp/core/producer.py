#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu.exceptions import ChannelError
from kombu import Producer as BaseProducer
from namekox_amqp.exceptions import MethodNotFound
from namekox_core.core.friendly import ignore_exception
from namekox_core.exceptions import gen_exc_to_data, gen_data_to_exc


class Producer(BaseProducer):
    def raise_again(self, errs):
        raise gen_data_to_exc(errs)

    def publish(self, *args, **kwargs):
        def succ():
            return super(Producer, self).publish(*args, **kwargs)

        def fail(e):
            exc_type, exc_value, exc_trace = e
            msg = str(exc_value)
            self.raise_again(gen_exc_to_data(MethodNotFound(msg)))

        return ignore_exception(succ, exc_func=fail, expected_exceptions=(ChannelError,))()
