from CaseBonita.Data.Consts import EventFields, PlatformName
from CaseBonita.Infrastructure.Consts import EntityNames, EventNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory
from CaseBonita.Infrastructure.ServiceHandler import BaseServiceHandler
from CaseBonita.Services.ManagementLayer.PlaylistsManager import PlaylistsDbManagement
from CaseBonita.Services.PlaylistDownloader.Factory import DownloaderFactory


class RouterHandler(BaseServiceHandler):
    @classmethod
    def get_service_queues(cls):
        queues = [QueueFactory.get_queue(entity_name=EntityNames.PLAYLIST_DOWNLOADER, action=Actions.FINISHED),
                  QueueFactory.get_queue(entity_name=EntityNames.PLAYLIST_UPLOADER, action=Actions.FINISHED)]
        return queues

    @classmethod
    def _process_msg(cls, msg):
        event_name = msg[EventFields.EVENT_NAME]
        if event_name == EventNames.PLAYLIST_DOWNLOAD_FINISHED:
            cls.handle_download_finished(msg)
        elif(event_name == EventNames.PLAYLIST_UPLOADER_FINISHED):
            cls.handle_uploader_finished(msg)

    @classmethod
    def handle_download_finished(cls, msg):
        upload_requested_topic = TopicFactory.get_topic(entity_name=EntityNames.PLAYLIST_UPLOADER,
                                                      action=Actions.REQUESTED)
        destination_platform = msg[EventFields.DESTINATION_PLATFORM]
        user_name = msg[EventFields.USER_NAME]
        playlist_url = msg[EventFields.PLAYLIST_URL]
        upload_requested_msg = {
            EventFields.EVENT_NAME: EventNames.PLAYLIST_UPLOADER_REQUESTED,
            EventFields.USER_NAME: user_name,
            EventFields.PLAYLIST_URL: playlist_url,
            EventFields.DESTINATION_PLATFORM: destination_platform,
        }
        upload_requested_topic.publish(upload_requested_msg)

    @classmethod
    def handle_uploader_finished(cls):
        pass







