from CaseBonita.Data.Consts import EventFields
from CaseBonita.Infrastructure.Consts import EntityNames, EventNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory
from CaseBonita.Infrastructure.ServiceHandler import BaseServiceHandler
from CaseBonita.Services.ManagementLayer.PlaylistsManager import PlaylistsDbManagement
from CaseBonita.Services.PlaylistDownloader.Factory import DownloaderFactory


class PlaylistDownloaderHandler(BaseServiceHandler):
    @classmethod
    def get_service_queues(cls):
        queues = [QueueFactory.get_queue(entity_name=EntityNames.PLAYLIST_DOWNLOADER, action=Actions.REQUESTED)]
        return queues

    @classmethod
    def _process_msg(cls, msg):
        event_name = msg[EventFields.EVENT_NAME]
        if event_name == EventNames.PLAYLIST_DOWNLOAD_REQUESTED:
            cls.handle_download_playlist(msg)

    @classmethod
    def handle_download_playlist(cls, msg):
        source_url = msg[EventFields.SOURCE_URL]
        source_platform = msg[EventFields.SOURCE_PLATFORM]
        handler = DownloaderFactory.get_handler(source_platform)
        playlist = handler(source_url, source_platform).download_playlist()
        PlaylistsDbManagement.insert_playlist_to_db(playlist, source_platform, source_url)
        download_finished_topic = TopicFactory.get_topic(entity_name=EntityNames.PLAYLIST_DOWNLOADER,
                                                         action=Actions.FINISHED)
        finished_msg = {
            EventFields.EVENT_NAME: EventNames.PLAYLIST_DOWNLOAD_FINISHED
        }
        download_finished_topic.publish(finished_msg)
        print('finished downloading playlist, printing results')
        print(playlist)
