# A lot more explicit to call it like this, I recommend to keep as a project convention.
from spotipy import Spotify as SpotifyApiClient
from spotipy import prompt_for_user_token

from CaseBonita.Data.Consts import Spotify, ITEMS, NAME, OWNER, ID, ARTIST, TRACK


class SpotifyConnector:
    """
    This class is used to return a user authenticated spotipy's Spotify API client.
    """
    username = None
    spotify = None
    LOCAL_SERVER = 'http://127.0.0.1:7000/'

    @classmethod
    def return_auth_client(cls, user_name):
        """
        This method opens a prompt for user to connect to spotify.
        If authorized by the user, they'll be redirected to a predefined redirected URI with an authentication token
        attached to it.
        :rtype str: the striped authentication token.
        """
        cls.username = user_name
        token = prompt_for_user_token(client_id=Spotify.CLIENT_ID,
                                      client_secret=Spotify.CLIENT_SECRET,
                                      redirect_uri=cls.LOCAL_SERVER,
                                      scope=Spotify.SPOTIFY_ACCESS_SCOPE,
                                      username=cls.username)

        cls.spotify = SpotifyApiClient(auth=token)
        return cls.spotify

    @classmethod
    def get_playlist_id(cls, playlist_name):
        """
        This method gets all of the user playlists and checks if anyone of them matches the given playlist name.
        if it does, it returns it's id.
        :param playlist_name: the playlist to be matched.
        """
        # As this method would be useful for uploader and downloader, why not put here as well (previously on spotify
        # upload handler)
        user_playlists = cls.spotify.user_playlists(limit=50, user=cls.username)
        try:
            playlist_id = [playlist[OWNER][ID] for playlist in user_playlists[ITEMS] if
                           playlist_name.lower() in playlist[NAME].lower()]
            return playlist_id
        except KeyError('Was not able to match given playlist names to existing ones, please check it.') as e:
            print(e)

    def get_tracks_id(self, song):
        artist = song[0]
        track = song[1]
        track_id = self.spotify.search(q=ARTIST + artist + TRACK + track, type=TRACK)
        return track_id

    @classmethod
    def write_auth_token_to_db(cls):
        # TODO: spotipy's connection function generates a cache file per user containing the user's auth token and
        #  it's expiration.
        #  Maybe wed'e like to send to the db? in the case of connection disruption or user returning in under an hour
        #  we could just call it instead of reinstating the process.
        pass

