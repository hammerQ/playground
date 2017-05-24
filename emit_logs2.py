#!/usr/bin/env python
import pika
import sys

# setup connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# setup exchange
channel.exchange_declare(exchange='direct_logs',
                         type='direct')

# construct message
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# publish
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()