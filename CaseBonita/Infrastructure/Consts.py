RABBIT_MQ_HOST = 'localhost'

class EntityNames(object):
    "This will be used to create queues from - each entity will have queue for each action type"
    PLAYLIST_DOWNLOADER = 'PLAYLIST-DOWNLOADER'
    PLAYLIST_UPLOADER = 'PLAYLIST_UPLOADER'
    INITIATOR = 'INITIATOR'

class Actions(object):
    REQUESTED = 'REQUESTED'
    FINISHED = 'FINISHED'
