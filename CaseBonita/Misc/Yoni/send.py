from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Infrastructure.Consts import EntityNames, Actions, EventNames
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory

if __name__ == '__main__':
    source_url = "https://music.apple.com/il/playlist/shiras-18th-birthday/pl.u-9N9L24LIx3DZ3K0"
    platform_name = PlatformName.APPLE_MUSIC
    msg = {
        'source_url': source_url,
        'source_platform': platform_name,
        'event_name': EventNames.PLAYLIST_DOWNLOAD_REQUESTED
    }
    topic = TopicFactory.get_topic(EntityNames.PLAYLIST_DOWNLOADER, action=Actions.REQUESTED)
    topic.publish(msg)
