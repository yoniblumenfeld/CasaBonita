class PlatformName(object):
    SPOTIFY = 'spotify'
    APPLE_MUSIC = 'apple_music'
    DEEZER = 'deezer'


CHROMEDRIVER = "/home/yovel/PycharmProjects/chromedriver"
APPLEMUSIC_LOGIN_PAGE = 'https://music.apple.com/us/artist/login/439834157'


# For development server


class Spotify(object):
    CLIENT_ID = 'c13f9174976545dc88adabebe21d7e56'
    CLIENT_SECRET = '4ebe64f377994602b0ebf12232ab4d2b'
    SPOTIFY_ACCESS_SCOPE = 'playlist-modify-private'


INDEX = 0

TRACK = 'track'
TITLE = 'title'
ARTIST = 'artist'
TRACK_ID = 'track_id'
ID = 'id'
OWNER = 'owner'
NAME = 'name'
ITEMS = 'items'


class MongoCollections(object):
    PLAYLISTS = 'playlists'


class EventFields(object):
    EVENT_NAME = 'event_name'
    SOURCE_URL = 'source_url'
    SOURCE_PLATFORM = 'source_platform'


PLAYLIST = 'playlist'
PLATFORM = 'platform'
PLAYLIST_URL = 'playlist_url'
TIMESTAMP = 'timestamp'

SPOTIFY_ACCESS_SCOPE = 'playlist-modify-private'
