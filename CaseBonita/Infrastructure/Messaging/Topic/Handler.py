import json
from CaseBonita.Infrastructure.Messaging.Channel.Factory import ChannelFactory

class TopicHandler(object):
    def __init__(self, entity_name, action):
        self._channel = ChannelFactory.get_channel_handler(entity_name, action)
        self._topic_name = f'{entity_name}_{action}'

    def publish(self, msg):
        msg = json.dumps(msg)
        self._channel.publish(msg, routing_key=self._topic_name)
