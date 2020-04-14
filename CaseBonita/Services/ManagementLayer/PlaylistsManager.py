from datetime import datetime

from CaseBonita.Data.Consts import PLAYLIST, PLATFORM, PLAYLIST_URL, TIMESTAMP, MongoCollections
from CaseBonita.Infrastructure.DB.MongoDB.Connector import MongoConnector


class PlaylistsDbManagement:
    @classmethod
    def insert_playlist_to_db(cls, playlist, platform, playlist_url):
        document = {
            PLAYLIST: playlist,
            PLATFORM: platform,
            PLAYLIST_URL: playlist_url,
            TIMESTAMP: datetime.utcnow()
        }
        MongoConnector().insert_document_into_collection(document, MongoCollections.PLAYLISTS)

    @classmethod
    def find_playlist(cls, playlist_url):
        query = {
            PLAYLIST_URL: playlist_url
        }
        return MongoConnector().find_documents_in_collection(query, MongoCollections.PLAYLISTS)
