from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST
from CaseBonita.Infrastructure.Messaging.Factory import ChannelFactory, TopicFactory

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
    topic = TopicFactory.get_topic(channel, exchange_name, routing_key=routing_key)
    topic.publish('Test Success!')