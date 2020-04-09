from CaseBonita.Infrastructure.Messaging.Channel.Handler import ChannelHandler
from CaseBonita.Infrastructure.Messaging.Connection.Factory import ConnectionFactory


class ChannelFactory(object):
    _channels = {}

    @classmethod
    def get_channel_handler(cls, entity_name, action):
        identifier = (entity_name, action)
        channel = cls._channels.get(identifier, None)
        if channel is None:
            connection = ConnectionFactory.get_connection_handler(action)
            channel = ChannelHandler(connection, entity_name)
        cls._channels[identifier] = channel
        return channel
