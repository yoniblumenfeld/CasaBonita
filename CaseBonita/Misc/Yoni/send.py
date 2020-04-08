import json

from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Infrastructure.Consts import RABBIT_MQ_HOST, EntityNames, Actions
from CaseBonita.Infrastructure.Messaging.Channel.Factory import ChannelFactory
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory

if __name__ == '__main__':
    entity_name = EntityNames.PLAYLIST_DOWNLOADER
    action = Actions.REQUESTED
    channel = ChannelFactory.get_channel_handler(entity_name, action)
    topic = TopicFactory.get_topic(entity_name, action)
    msg = {
        'source_url': "https://music.apple.com/il/playlist/shiras-18th-birthday/pl.u-9N9L24LIx3DZ3K0",
        'source_platform': PlatformName.APPLE_MUSIC
    }
    topic.publish(msg)