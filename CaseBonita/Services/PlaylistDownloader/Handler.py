import json

from CaseBonita.Infrastructure.Consts import EntityNames, EventNames
from CaseBonita.Infrastructure.ServiceHandler import BaseServiceHandler
from CaseBonita.Services.PlaylistDownloader.Factory import DownloaderFactory


class PlaylistDownloaderHandler(BaseServiceHandler):
    @classmethod
    def get_entity_name(cls):
        return EntityNames.PLAYLIST_DOWNLOADER

    @classmethod
    def _process_msg(cls, msg):
        msg = json.loads(msg)
        event_name = msg['event_name']
        if event_name == EventNames.PLAYLIST_DOWNLOAD_REQUESTED:
            cls.handle_download_playlist(msg)

    @classmethod
    def handle_download_playlist(cls, msg):
        source_url = msg['source_url']
        source_platform = msg['source_platform']
        handler = DownloaderFactory.get_handler(source_platform)
        playlist = handler(source_url, source_platform).download_playlist()
        print('finished downloading playlist, printing results')
        print(playlist)
