from CaseBonita.Infrastructure.Consts import Actions, RABBIT_MQ_HOST
from CaseBonita.Infrastructure.Messaging.Connection.Handler import ConnectionHandler
from CaseBonita.Utils.ClassUtils import get_class_upper_variables


class ConnectionFactory(object):
    _connections = { action:ConnectionHandler(RABBIT_MQ_HOST) for action in get_class_upper_variables(Actions)}

    @classmethod
    def get_connection_handler(cls, action):
        connection = cls._connections.get(action, None)
        if connection is None:
            raise KeyError('No such action in the system - connections are mapped using action to connection')
        return connection
