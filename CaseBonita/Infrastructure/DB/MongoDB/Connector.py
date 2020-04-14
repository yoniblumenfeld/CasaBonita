from datetime import datetime
import pymongo
from CaseBonita.Data.Database import MongoDB


class MongoConnector:
    _connection = None

    def __init__(self, db=MongoDB.RODO_DB):
        self._db = db

    @property
    def connection(self):
        """
        :rtype: pymongo.MongoClient:
        """
        if self._connection is None:
            self._connection = pymongo.MongoClient('localhost', 27017)
        return self._connection

    def insert_documents_into_collection(self, docs, collection_name):
        """
        This function inserts documents list into a collection
        :param list docs: documents list
        :param str collection_name:
        """
        collection = self.connection[self._db][collection_name]
        collection.insert_many(docs)

    def insert_document_into_collection(self, doc, collection_name):
        """
        This function inserts a document into a collection
        :param dict doc: document
        :param str collection_name:
        """
        self.insert_documents_into_collection([doc], collection_name)

    def find_documents_in_collection(self, query, collection_name):
        """
        :param dict query:
        :param str collection_name:
        :rtype: list: results list
        """
        if query is None:
            query = {}
        collection = self.connection[self._db][collection_name]
        result = collection.find(query)
        return result


if __name__ == '__main__':
    test_doc = [{
        'platform': "test_platform",
        'playlist_url': 'test_playlist_url.com',
        'playlist': [
            {
                'title': "DoMe",
                'artist': "Please"
            }
        ],
        'timestamp': datetime.utcnow()
    }]
    playlists_collection = 'playlists'
    MongoConnector(MongoDB.RODO_DB).insert_documents_into_collection(test_doc, playlists_collection)
    pass




