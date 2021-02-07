#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from kombu import Producer as BaseProducer


class Producer(BaseProducer):
    def publish(self, *args, **kwargs):
        return super(Producer, self).publish(*args, **kwargs)
