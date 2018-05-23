# -*- coding: utf-8 -*-
import logging
import os
import traceback

from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.internet import reactor, protocol, error
from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate

from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.python import log

from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate

import txamqp.spec
import txamqp.spec

RABBITMQ_DEFAULT_HOST = 'rabbitmq.cluster1.master'

QUEUE_SERVER = ['rabbitmq.cluster1.master', 'rabbitmq.cluster2.master']

RABBITMQ_CONNECT_INFO = {
    'host': 'rabbitmq.cluster1.master',
    'port': 5672,
    'vhost': '/',
    'username': 'backend',
    'password': 'backend',
    'spec': 'amqp0-9-1.stripped.xml',
}


@inlineCallbacks
def gotConnection(conn, username, password):
    print("Connected to broker.")
    yield conn.authenticate(username, password)

    print("Authenticated. Ready to receive messages")
    chan = yield conn.channel(1)
    yield chan.channel_open()

    yield chan.queue_declare(queue="chatrooms", durable=True, exclusive=False, auto_delete=False)
    yield chan.exchange_declare(exchange="chatservice", type="direct", durable=True, auto_delete=False)

    yield chan.queue_bind(queue="chatrooms", exchange="chatservice", routing_key="txamqp_chatroom")

    yield chan.basic_consume(queue='chatrooms', no_ack=True, consumer_tag="testtag")

    queue = yield conn.queue("testtag")

    while True:
        msg = yield queue.get()
        print('Received: {0} from channel #{1}'.format(msg.content.body, chan.id))
        if msg.content.body == "STOP":
            break

    yield chan.basic_cancel("testtag")

    yield chan.channel_close()

    chan0 = yield conn.channel(0)

    yield chan0.connection_close()

    reactor.stop()


if __name__ == "__main__":
    delegate = TwistedDelegate()
    d = ClientCreator(reactor, AMQClient, delegate=delegate, vhost=RABBITMQ_CONNECT_INFO['vhost'],
                      spec=RABBITMQ_CONNECT_INFO['spec']).connectTCP(RABBITMQ_CONNECT_INFO['host'],
                                                                     RABBITMQ_CONNECT_INFO['port'])

    d.addCallback(gotConnection, RABBITMQ_CONNECT_INFO['username'], RABBITMQ_CONNECT_INFO['password'])


    def whoops(err):
        if reactor.running:
            log.err(err)
            reactor.stop()


    d.addErrback(whoops)

    reactor.run()

# class txRabbitmq:
#     instances = {}
#
#     def __init__(self, host=RABBITMQ_DEFAULT_HOST):
#         self.channel = None
#         self.client = None
#         self.init_config(host)
#
#     def init_config(self, host):
#         if not RABBITMQ_CONNECT_INFO:
#             logging.error('not found config RABBITMQ_CONNECT_INFO')
#             os._exit(-1)
#         self.host = host
#         self.port = RABBITMQ_CONNECT_INFO['port']
#         self.vhost = RABBITMQ_CONNECT_INFO['vhost']
#         self.username = RABBITMQ_CONNECT_INFO['username']
#         self.password = RABBITMQ_CONNECT_INFO['password']
#         self.spec = RABBITMQ_CONNECT_INFO['spec']
#
#     @classmethod
#     def init_queues(cls, consumer_host=''):
#         for host in QUEUE_SERVER:
#             if host != consumer_host:
#                 mq = cls.get_instance(host=host)
#                 mq.init_queue()
#
#     @classmethod
#     def get_instance(cls, host=RABBITMQ_DEFAULT_HOST):
#         if cls.instances.get(host):
#             return cls.instances.get(host)
#         cls.instances[host] = txRabbitmq(host=host)
#         return cls.instances[host]
#
#     @inlineCallbacks
#     def connect(self):
#         host = self.host
#         port = self.port
#         spec = self.spec
#         user = self.username
#         password = self.password
#         vhost = self.vhost
#         delegate = TwistedDelegate()
#         onConn = Deferred()
#         p = AMQClient(delegate, vhost, txamqp.spec.load(spec), heartbeat=0)
#         f = protocol._InstanceFactory(reactor, p, onConn)
#         c = reactor.connectTCP(host, port, f)
#
#         def errb(thefailure):
#             thefailure.trap(error.ConnectionRefusedError)
#             logging.error(traceback.format_exc())
#
#         onConn.addErrback(errb)
#         client = yield onConn
#         self.client = client
#         yield self.authenticate(self.client, user, password)
#         returnValue(client)
#
#     @inlineCallbacks
#     def get_channel(self):
#         if not self.channel:
#             client = yield self.connect()
#             channel = yield self.open_channel(client)
#         returnValue(self.channel)
#
#     @inlineCallbacks
#     def authenticate(self, client, user, password):
#         yield client.authenticate(user, password)
#
#     @inlineCallbacks
#     def open_channel(self, client):
#         channel = yield client.channel(1)
#         channel.channel_open()
#         self.channel = channel
#         yield channel
#         returnValue(channel)
#
#     @inlineCallbacks
#     def init_queue(self):
#         try:
#             client = yield self.connect()
#             yield self.open_channel(client)
#             logging.info('init for service mq finish %s', self.host)
#         except:
#             logging.error(traceback.format_exc())
#
#
# if __name__ == '__main__':
#     txRabbitmq.init_queues()
#     reactor.run()
