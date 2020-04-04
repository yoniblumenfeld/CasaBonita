import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

from CaseBonita.Services.PlaylistUploader.Handlers.Base import BaseAPIUploader
from .consts import CLIENT_ID, CLIENT_SECRET


class UploadToSpotify(BaseAPIUploader):
    def __init__(self, developer_key, _songs_json_file, user_credentials):
        super(BaseAPIUploader, self).__init__(developer_key, _songs_json_file, user_credentials)

    def create_developer_credentials(self):
        credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.developer_key = sp.Spotify(client_credentials_manager=credentials_manager)
        return self.developer_key

    def get_tracks_id(self, artist, track):
        track_id = self.developer_key.search(q='artist:' + artist + ' track:' + track, type='track')
        self.songs_json_file = self.songs_json_file.update('track_id':track_id)
        return self.songs_json_file

    def create_playlist(self, playlist_name):
        token = self.developer_key.user_playlist_create(user=self.user_credentials['username'],
                                                        name=playlist_name,
                                                        public=True)
        return token
