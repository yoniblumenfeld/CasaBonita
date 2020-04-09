from CaseBonita.Infrastructure.Consts import EntityNames, EventNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory
from CaseBonita.Infrastructure.ServiceHandler import BaseServiceHandler
from CaseBonita.Services.PlaylistDownloader.Factory import DownloaderFactory


class PlaylistDownloaderHandler(BaseServiceHandler):
    @classmethod
    def get_service_queues(cls):
        queues = [QueueFactory.get_queue(entity_name=EntityNames.PLAYLIST_DOWNLOADER, action=Actions.REQUESTED)]
        return queues

    @classmethod
    def _process_msg(cls, msg):
        event_name = msg['event_name']
        if event_name == EventNames.PLAYLIST_DOWNLOAD_REQUESTED:
            cls.handle_download_playlist(msg)

    @classmethod
    def handle_download_playlist(cls, msg):
        source_url = msg['source_url']
        source_platform = msg['source_platform']
        handler = DownloaderFactory.get_handler(source_platform)
        playlist = handler(source_url, source_platform).download_playlist()
        download_finished_topic = TopicFactory.get_topic(entity_name=EntityNames.PLAYLIST_DOWNLOADER,
                                                         action=Actions.FINISHED)
        # TODO: add writing to db
        finished_msg = {
            'event_name': EventNames.PLAYLIST_DOWNLOAD_FINISHED
        }
        download_finished_topic.publish(finished_msg)
        print('finished downloading playlist, printing results')
        print(playlist)
