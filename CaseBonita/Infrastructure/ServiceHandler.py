from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory


class BaseServiceHandler(object):
    @classmethod
    def get_entity_name(cls):
        """
        :rtype: str: entity name
        """
        raise NotImplementedError

    @classmethod
    def _listen_to_entity_queues(cls):
        """
        This method uses the entity name configured for the service handler, and listens the queues relevant to it.
        """
        entity_name = cls.get_entity_name()
        queues = QueueFactory.get_entity_queues(entity_name)
        for queue in queues:
            queue.consume(cls.process_messages)

    @classmethod
    def process_messages(cls, ch, method, properties, body):
        cls._process_msg(body)

    @classmethod
    def _process_msg(cls, msg):
        """
        This method should be implemented for each service handler and should contain the logic
        to deal with each msg type (event type).
        :param dict msg:
        """
        raise NotImplementedError

    @classmethod
    def run(cls):
        cls._listen_to_entity_queues()
