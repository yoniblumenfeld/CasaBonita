import json

from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Infrastructure.Consts import EntityNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory
from CaseBonita.Services.PlaylistDownloader import Factory

def callback(ch, method, properties, body):
    body = json.loads(body)
    source_url = body['source_url']
    source_platform = body['source_platform']
    handler = Factory.DownloaderFactory.get_handler(source_platform)
    playlist = handler(source_url, source_platform).download_playlist()
    print('finished downloading playlist, printing results')
    print(playlist)


if __name__ == '__main__':
    # source_url = "https://music.apple.com/il/playlist/shiras-18th-birthday/pl.u-9N9L24LIx3DZ3K0"
    # handler(source_url, source_platform).download_playlist()
    entity_name = EntityNames.PLAYLIST_DOWNLOADER
    action = Actions.REQUESTED
    queue = QueueFactory.get_queue(entity_name, action)
    queue.consume(callback)
