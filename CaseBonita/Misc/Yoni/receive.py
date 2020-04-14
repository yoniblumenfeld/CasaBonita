from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST, EntityNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory

if __name__ == '__main__':
    entity_name = EntityNames.PLAYLIST_DOWNLOADER
    action = Actions.REQUESTED
    queue = QueueFactory.get_queue(entity_name, action)
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
    queue.consume(callback)

