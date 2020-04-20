from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from CaseBonita.Data.Consts import ARTIST, TRACK, ITEMS, NAME, OWNER, ID, TRACK_ID
from CaseBonita.Services.PlaylistUploader.Handlers.Base import BaseAPIUploader
from CaseBonita.Services.PlaylistUploader.Handlers.Consts import CLIENT_ID, CLIENT_SECRET, LOCAL_SERVER, SCOPE
from CaseBonita.Utils.RequestUtils import retry_request


class UploadToSpotify(BaseAPIUploader):
    def __init__(self, _songs_json_file, user_name):
        super(BaseAPIUploader, self).__init__(_songs_json_file)
        self.spotify = Spotify(auth=self.connect_spotify_api())
        self.user_name = user_name

    LOCAL_SERVER = 'http://0.0.0.0:7000/'
    access_token = None

    def connect_spotify_api(self):
        """
        This method uses spotipy's client to connect to a user.
        """
        auth = SpotifyOAuth(client_secret=CLIENT_SECRET,
                            client_id=CLIENT_ID,
                            username=self.user_name,
                            scope=SCOPE,
                            redirect_uri=LOCAL_SERVER
                            )
        return auth

    def set_access_token(self):
        """
        This method connects checks if an access token exists in cache or receives a new one from spotify.
        :returns self.access_token str:
        """
        self.access_token = self.connect_spotify_api().get_access_token(as_dict=False)
        return self.access_token

    def get_tracks_id(self, artist, track):
        """
        get's the given track track id, to be ran on every song in the json file.
        """
        track_id = self.spotify.search(q=f'{ARTIST}:' + artist + f' {TRACK}:' + track, type='track')
        self.songs_json_file = self.songs_json_file.update('track_id':track_id)
        return self.songs_json_file

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

    def insert_songs_to_playlist(self):
        """
        This method initiates the insert new playlist and takes the given name from it.
        it then lists all the tracks ids and uploads them to the playlist.
        """
        playlist, playlist_name = self.insert_new_playlist()
        tracks_ids_list = list(self.songs_json_file[TRACK_ID])
        upload_songs_to_playlist = self.spotify.user_playlist_add_tracks(user=self.user_name,
                                                                         tracks=tracks_ids_list,
                                                                         playlist_id=self.get_playlist_id(playlist_name)
                                                                         )
        return upload_songs_to_playlist
