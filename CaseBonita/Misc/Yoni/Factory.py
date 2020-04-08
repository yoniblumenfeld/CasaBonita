import json

import pika
from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST


class Connection(object):
    _connection = None
    def __init__(self, host=RABBIT_MQ_HOST):
        self._host=host

    def _is_connection_active(self):
        if self._connection is None:
            return False
        #TODO: ADD logic to determine if connection is up
        return True

    def __call__(self, *args, **kwargs):
        if self._is_connection_active():
            return self._connection
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host)
        )
        return self._connection


class Channel(object):
    def _is_channel_active(self):
        if self._channel is None:
            return False
        #TODO: ADD logic to determine if channel is up
        return True

    @property
    def channel(self):
        if self._is_channel_active():
            return self._channel
        connection = self._connection()
        self._channel = connection.channel()
        return self._channel

    def __init__(self, connection):
        self._connection = connection
        self._channel = None

    def __call__(self, *args, **kwargs):
        return self.channel

    def decalre_queue(self, queue_name, **kwargs):
        self.channel.queue_declare(queue_name, **kwargs)

    def bind_queue(self, exchange_name, queue_name, binding_key):
        self._channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=binding_key
        )

    def declare_exchange(self, exchange_name, exchange_type='topic'):
        channel = self.channel
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type
        )


class ChannelFactory(object):
    channels_cache = {}

    @classmethod
    def get_channel_identifier(cls, entity_name, host):
        return f'{host}.{entity_name}'

    @classmethod
    def get_channel(cls, channel_id):
        if channel_id in cls.channels_cache:
            return cls.channels_cache[channel_id]
        raise KeyError('No such channel')


class ConnectionFactory(object):
    connections_cache = {}

    @classmethod
    def get_connection_identifier(cls, host):
        return host

    @classmethod
    def get_connection(cls, connection_id):
        if connection_id in cls.connections_cache:
            print('taking connection from cache')
            return cls.connections_cache[connection_id]
        raise KeyError('No such connection')




class Queue(object):
    def __init__(self, channel, queue_name):
        self._channel = channel
        self._queue_name = queue_name

    def consume(self, callback):
        self._channel.basic_consume(queue=self._queue_name,
                                    on_message_callback=callback,
                                    auto_ack=True)
        self._channel.start_consuming()


class QueueFactory(object):
    queues_cache = {}

    @classmethod
    def get_queue(cls, queue_name, channel=None):
        if queue_name in cls.queues_cache:
            return cls.queues_cache[queue_name]
        if channel is None:
            raise ConnectionError('if no queue in cache must pass channel')
        cls.queues_cache[queue_name] = Queue(channel, queue_name)
        return cls.queues_cache[queue_name]


class Topic(object):
    def __init__(self, channel, exchange_name, routing_key):
        self._channel = channel
        self._exchange_name = exchange_name
        self._routing_key = routing_key

    def publish(self, msg):
        msg = json.dumps(msg)
        self._channel().basic_publish(exchange=self._exchange_name,
                                    routing_key=self._routing_key,
                                    body=msg)


class TopicFactory(object):
    topic_cache = {}

    @classmethod
    def get_topic_id(cls, exchange_name, routing_key):
        return f'{exchange_name}.{routing_key}'

    @classmethod
    def _get_topic(cls, topic_id, channel=None, exchange_name=None, routing_key=None):
        if topic_id in cls.topic_cache:
            return cls.topic_cache[topic_id]
        if (channel is None) or (exchange_name is None) or (routing_key is None):
            raise Exception('missing parameter to set topic, couldnt find one in cache')
        topic = Topic(channel, exchange_name, routing_key)
        cls.topic_cache[topic_id] = topic
        return topic

    @classmethod
    def get_topic(cls, entity_name, action):
        topic_id = cls.get_topic_id(exchange_name=entity_name,
                                    routing_key=action)

