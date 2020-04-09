from CaseBonita.Infrastructure.Consts import Actions
from CaseBonita.Utils.ClassUtils import get_class_upper_variables


class ChannelHandler(object):
    def __init__(self, connection, entity_name, queues_list=None):
        """
        :param ConnectionHandler connection:
        """
        self._connection = connection.get_connection()
        self._channel = None # lazy init
        self._exchange_name = entity_name
        self._queues = queues_list or [f'{entity_name}_{action}' for action in get_class_upper_variables(Actions)]

    def get_channel(self):
        return self.channel

    @property
    def channel(self):
        if self._channel is None:
            self._flush_channel()
            self._flush_queues()
        return self._channel

    def _flush_channel(self):
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange_name,
                                       exchange_type='topic')

    def _flush_queues(self):
        for queue in self._queues:
            self.add_queue(queue, force=True)

    def add_queue(self, queue, force=False):
        if not force: #  Force occurs when channel was restarted or flushed and has to be recreated with appropriate queues
            if queue in self._queues:
                return
        if queue not in self._queues:
            self._queues.append(queue)
        self.channel.queue_declare(queue)
        self._channel.queue_bind(
            exchange=self._exchange_name,
            queue=queue,
            routing_key=queue
        )

    def publish(self, json_msg, routing_key):
        self.channel.basic_publish(exchange=self._exchange_name,
                                   routing_key=routing_key,
                                   body=json_msg)
