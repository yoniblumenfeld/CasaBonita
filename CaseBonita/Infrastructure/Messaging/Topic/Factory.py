from CaseBonita.Infrastructure.Messaging.Topic.Handler import TopicHandler


class TopicFactory(object):
    _topics = {}

    @classmethod
    def get_topic(cls, entity_name, action):
        identifier = (entity_name, action)
        if identifier in cls._topics:
            return cls._topics[identifier]
        topic = TopicHandler(entity_name, action)
        cls._topics[identifier] = topic
        return topic
