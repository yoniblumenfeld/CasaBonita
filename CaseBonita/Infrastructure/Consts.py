RABBIT_MQ_HOST = 'localhost'

class EntityNames(object):
    "This will be used to create queues from - each entity will have queue for each action type"
    PLAYLIST_DOWNLOADER = 'PLAYLIST-DOWNLOADER'
    PLAYLIST_UPLOADER = 'PLAYLIST_UPLOADER'
    INITIATOR = 'INITIATOR'


class Actions(object):
    REQUESTED = 'REQUESTED'
    FINISHED = 'FINISHED'


class EventNames(object):
    PLAYLIST_DOWNLOAD_REQUESTED = 'PLAYLIST_DOWNLOAD_REQUESTED'
    PLAYLIST_DOWNLOAD_FINISHED = 'PLAYLIST_DOWNLOAD_FINISHED'
