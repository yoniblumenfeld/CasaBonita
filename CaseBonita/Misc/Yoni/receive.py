#!/usr/bin/env python
from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST
from CaseBonita.Infrastructure.Messaging.Factory import ChannelFactory, QueueFactory

if __name__ == '__main__':
    channel = ChannelFactory.get_channel(host=RABBIT_MQ_HOST)
    queue_name = 'test_queue'
    exchange_name = 'try'
    routing_key = 'all.me'
    exchange_type = 'topic'
    channel.decalre_queue(queue_name=queue_name)
    channel.declare_exchange(exchange_name=exchange_name,
                             exchange_type=exchange_type)
    channel.bind_queue(exchange_name=exchange_name, queue_name=queue_name,
                       binding_key=routing_key)
    queue = QueueFactory.get_queue(queue_name,
                           channel)


    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    queue.consume(callback=callback)
