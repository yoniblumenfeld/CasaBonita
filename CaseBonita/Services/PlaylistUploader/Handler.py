from CaseBonita.Data.Consts import EventFields
from CaseBonita.Infrastructure.Consts import EntityNames, EventNames, Actions
from CaseBonita.Infrastructure.Messaging.Queue.Factory import QueueFactory
from CaseBonita.Infrastructure.Messaging.Topic.Factory import TopicFactory
from CaseBonita.Infrastructure.ServiceHandler import BaseServiceHandler
from CaseBonita.Services.PlaylistUploader.Factory import UploaderFactory


class PlaylistUploaderHandler(BaseServiceHandler):
    @classmethod
    def get_service_queues(cls):
        queues = [QueueFactory.get_queue(entity_name=EntityNames.PLAYLIST_UPLOADER, action=Actions.REQUESTED)]
        return queues

    @classmethod
    def _process_msg(cls, msg):
        event_name = msg[EventFields.EVENT_NAME]
        if event_name == EventNames.PLAYLIST_UPLOAD_REQUESTED:
            cls.handle_upload_playlist(msg)

    @classmethod
    def handle_upload_playlist(cls, msg):
        destination_platform = msg[EventFields.DESTINATION_PLATFORM]
        handler = UploaderFactory.get_handler(destination_platform)
        upload_playlist = handler(destination_platform).upload_playlist()
        upload_finished_topic = TopicFactory.get_topic(entity_name=EntityNames.PLAYLIST_UPLOADER,
                                                       action=Actions.FINISHED)
        finished_msg = {
            EventFields.EVENT_NAME: EventNames.PLAYLIST_UPLOAD_FINISHED
        }
        upload_finished_topic.publish(finished_msg)
        print('playlist upload is completed')
