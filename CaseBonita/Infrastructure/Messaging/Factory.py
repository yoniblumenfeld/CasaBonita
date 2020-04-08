import pika
from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST
from CaseBonita.Services.PlaylistDownloader.Factory import DownloaderFactory


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
    _channel = None
    def _is_channel_active(self):
        if self._channel is None:
            return False
        #TODO: ADD logic to determine if channel is up
        return True

    def __init__(self, connection):
        self._connection = connection

    def __call__(self, *args, **kwargs):
        if self._is_channel_active():
            return self._channel
        connection = self._connection()
        self._channel = connection.channel()
        return self._channel

def Exchange(object):
    _exchange = None

class ConnectionFactory(object):
    connections_cache = {}

    @classmethod
    def get_connection(cls, host=RABBIT_MQ_HOST):
        if host in cls.connections_cache:
            return cls.connections_cache[host]
        connection = Connection(host)
        cls.connections_cache[host] = connection
        return connection


class ChannelFactory(object):
    channels_cache = {}

    @classmethod
    def get_channel(cls, host):
        if host in cls.channels_cache:
            return cls.channels_cache[host]
        connection = ConnectionFactory.get_connection(host)
        channel = Channel(connection)
        cls.channels_cache[host] = channel
        return channel


class ExchangeFactory(object):
    exchange_cache = {}

    @classmethod
    def _get_exchange_identifier(cls, host, exchange_name, exchange_type):
        return f'{host}.{exchange_name}.{exchange_type}'

    @classmethod
    def get_exchange(cls, host, exchange_name, exchange_type='topic'):
        identifier = cls._get_exchange_identifier(host, exchange_name, exchange_type)
        if identifier in cls.exchange_cache:
            return cls.exchange_cache[identifier]
        channel = ChannelFactory.get_channel(host)
        exchange = channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
        )
        cls.exchange_cache[identifier] = exchange
        return exchange

class QueueFactory(object):
    queues_cache = {}
    @classmethod
    def get_queue(cls):
        pass

class TopicFactory(object):
    @classmethod
    def get_topic(cls, entity_name, action):
        pass


def Handler(object):
    def _process_message(json_message):
        event_name = json_message['event_name']
        if event_name == 'PLAYLIST_DOWNLOAD_REQUESTED':
            platform_name = json_message['platform_name']
            source_url = json_message['source_url']
            downloader = DownloaderFactory.get_handler(platform_name)
            downloader.run()