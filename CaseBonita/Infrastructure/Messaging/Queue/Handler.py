from CaseBonita.Infrastructure.Messaging.Channel.Factory import ChannelFactory

class QueueHandler(object):
    def __init__(self, entity_name, action):
        self._queue_name = f'{entity_name}_{action}'
        self._channel = ChannelFactory.get_channel_handler(entity_name, action)

    def consume(self, callback):
        channel = self._channel.get_channel()
        channel.basic_consume(queue=self._queue_name,
                              on_message_callback=callback,
                              auto_ack=True)
        channel.start_consuming()
