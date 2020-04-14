import json


class BaseServiceHandler(object):
    @classmethod
    def get_service_queues(cls):
        """
        :rtype: list: list of queues to listen to
        """
        raise NotImplementedError

    @classmethod
    def _listen_to_queues(cls):
        """
        This method uses the entity name configured for the service handler, and listens the queues relevant to it.
        """
        queues = cls.get_service_queues()
        for queue in queues:
            queue.consume(cls.process_messages)

    @classmethod
    def process_messages(cls, ch, method, properties, body):
        cls._process_msg(json.loads(body))

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
        cls._listen_to_queues()
