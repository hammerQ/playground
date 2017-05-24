#!/usr/bin/env python
import pika
import sys

# setup connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# setup exchange
channel.exchange_declare(exchange='logs',
                         type='fanout')

# construct message
message = ' '.join(sys.argv[1:]) or "Hello World!"

# publish
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()




