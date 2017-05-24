#!/user/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

# setup queue w/o a name
result = channel.queue_declare(exclusive=True)

# create binding of queue and exchange
channel.queue_bind(exchange='logs', queue=result.method.queue)
queue_name = result.method.queue

print(' [x] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print( " [x] %r" % body)

channel.basic_consume (callback,
                       queue=queue_name,
                       no_ack=True)

channel.start_consuming()