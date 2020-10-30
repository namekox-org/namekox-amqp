#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from .rpc.handler import AMQPRpcHandler
from .sub.handler import AMQPSubHandler


amqp = type(__name__, (object,), {'rpc': AMQPRpcHandler.decorator, 'sub': AMQPSubHandler.decorator})
