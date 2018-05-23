# -*- coding: utf-8 -*-

import pika

credentials = pika.PlainCredentials('backend', 'backend')
parameters = pika.ConnectionParameters(host='172.16.10.161',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
print connection, channel
