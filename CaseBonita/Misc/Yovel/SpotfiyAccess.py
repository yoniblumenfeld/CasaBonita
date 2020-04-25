# A lot more explicit to call it like this, recommend to keep as project convention.
from spotipy import Spotify as SpotifyApiClient
from spotipy.util import prompt_for_user_token

from CaseBonita.Data.Consts import Spotify, ITEMS, NAME, OWNER, ID


class SpotifyConnector:
    """
    This class is used to return a user authenticated spotipy's Spotify API client.
    """
    username = None
    spotify = None

    @classmethod
    def get_access_to_user(cls, user_name):
        """
        This method opens a prompt for user to connect to spotify.
        If authorized by the user, they'll be redirected to a predefined redirected URI with an authentication token
        attached to it.
        :rtype str: the striped authentication token.
        """
        try:
            token = prompt_for_user_token(
                client_secret=Spotify.CLIENT_SECRET,
                client_id=Spotify.CLIENT_ID,
                username=user_name,
                scope=Spotify.SPOTIFY_ACCESS_SCOPE,
                redirect_uri='http://0.0.0.0:7000/'
            )
            # TODO: Find a way to pull the URL the user is redirected to.
            #       Some Rodo magical selenium touch would do the trick.
            auth_token = url.split("?code=")[1].split("&")[0]
            return auth_token
        except ConnectionError('was not able to retrieve auth token') as e:
            print(e)

    @classmethod
    def initiate_api_handler(cls, token):
        """
        Initiate a spotipy.Spotify object with the user's auth token, This object is used to interact with spotify's API
        and modify user's private data.
        :rtype Spotify Client object.
        """

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
            # Showing off some beasty list comprehension.
            playlist_id = [playlist[OWNER][ID] for playlist in user_playlists[ITEMS] if playlist_name in playlist[NAME]]
            return playlist_id
        except KeyError('Was not able to match given playlist names to existing ones, please check it.') as e:
            print(e)

    @classmethod
    def generate_songs_id_list(cls):
        #  TODO: as we know, in order to add songs to playlist we need the songs ids.
        #        Maybe we should put here?
        pass

    @classmethod
    def write_auth_token_to_db(cls):
        # TODO: spotipy's connection function generates a cache file per user containing the user's auth token and
        #  it's expiration.
        #  Maybe wed'e like to send to the db? in the case of connection disruption or user returning in under an hour
        #  we could just call it instead of reinstating the process.
        pass

    @classmethod
    def run(cls, user_name):
        spotify_api_client = cls.initiate_api_handler(cls.get_access_to_user(user_name=user_name))
        return spotify_api_client
