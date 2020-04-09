import json

from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Infrastructure.Consts import EntityNames, Actions
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory

if __name__ == '__main__':
    entity_name = EntityNames.PLAYLIST_DOWNLOADER
    action = Actions.REQUESTED
    topic = TopicFactory.get_topic(entity_name, action)
    msg = {
        'source_url': "https://music.apple.com/us/playlist/melvins-deep-cuts/pl.adc8f720731842f8ac2eaf6d00ac38bd?app=itunes",
        'source_platform': PlatformName.APPLE_MUSIC
    }
    topic.publish(msg)