from CaseBonita.Infrastructure.Messaging.Channel.Factory import ChannelFactory
from CaseBonita.Infrastructure.Messaging.Queue.Handler import QueueHandler
from CaseBonita.Utils.ClassUtils import get_class_upper_variables


class QueueFactory(object):
    _queues = {}

    @classmethod
    def insert_queue_to_factory(cls, entity_name, action):
        identifier = (entity_name, action)
        queue = QueueHandler(entity_name, action)
        cls._queues[identifier] = queue

    @classmethod
    def get_queue(cls, entity_name, action):
        identifier = (entity_name, action)
        if identifier in cls._queues:
            return cls._queues[identifier]
        cls.insert_queue_to_factory(entity_name, action)
        return cls._queues[identifier]
