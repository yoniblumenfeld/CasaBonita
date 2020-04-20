from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from CaseBonita.Data.Consts import ITEMS, NAME, OWNER, ID
from CaseBonita.Services.PlaylistUploader.Handlers.Base import BaseAPIUploader
from CaseBonita.Services.PlaylistUploader.Handlers.Consts import CLIENT_ID, CLIENT_SECRET, LOCAL_SERVER, SCOPE
from CaseBonita.Utils.RequestUtils import retry_request


class SpotifyUploadHandler(BaseAPIUploader):
    def __init__(self, _platform, spotify=None, user_name=None):
        super().__init__(_platform)
        self.spotify = spotify
        self.user_name = user_name

    LOCAL_SERVER = 'http://0.0.0.0:7000/'
    access_token = None

    def connect_to_spotify_api(self, user_name):
        """
        This method uses spotipy's client to connect to a user.
        """
        if self.spotify is None:
            auth = SpotifyOAuth(client_secret=CLIENT_SECRET,
                                client_id=CLIENT_ID,
                                username=self.user_name,
                                scope=SCOPE,
                                redirect_uri=LOCAL_SERVER,
                                cache_path='./cache.txt'
                                )
            self.spotify = Spotify(oauth_manager=auth)
            return self.spotify, auth

    def set_access_token(self, auth):
        """
        This method connects checks if an access token exists in cache or receives a new one from spotify.
        :returns self.access_token str:
        """
        self.access_token = auth.get_access_token(as_dict=False)
        return self.access_token

    @retry_request(total_retries=4)
    def insert_new_playlist(self, playlist_name):
        """
        Inserts a new playlist at the user's account.
        """
        playlist = self.spotify.user_playlist_create(user=self.user_name, name=playlist_name)
        return playlist, playlist_name

    def get_playlist_id(self, playlist_name):
        """
        This method gets all of the user playlists and checks if anyone of them matches the given playlist name.
        if it does, it returns it's id.
        :param playlist_name: the playlist to be matched.
        """
        user_playlists = self.spotify.user_playlists(limit=50, user=self.user_name)
        try:
            for playlist in user_playlists[ITEMS]:
                if playlist_name in playlist[NAME]:
                    playlist_id = playlist[OWNER][ID]
                    return playlist_id
        except KeyError('Was not able to match given playlist names to existing ones, please check it.') as e:
            print(e)

    def write_songs_to_playlist(self, songs_id, username):
        """
        This method initiates the insert new playlist and takes the given name from it.
        it then lists all the tracks ids and uploads them to the playlist.
        """
        client, auth = self.connect_to_spotify_api(username)
        self.set_access_token(auth=auth)
        playlist, playlist_name = self.insert_new_playlist(playlist_name='yo')
        print(playlist_name)
        upload_songs_to_playlist = self.spotify.user_playlist_add_tracks(user=username,
                                                                         tracks=songs_id,
                                                                         playlist_id=self.get_playlist_id(playlist_name)
                                                                         )
        return upload_songs_to_playlist


if __name__ == '__main__':
    username = 'oa7fxnn3xwxveug6000igp0v6'
    songs_id = ['7xGfFoTpQ2E7fRF5lN10tr']
    s = SpotifyUploadHandler(_platform='spotify')
    s.write_songs_to_playlist(songs_id=songs_id, username=username)
