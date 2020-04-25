from spotipy import Spotify, util

from CaseBonita.Data.Consts import ITEMS, NAME, OWNER, ID, ARTIST, TRACK, PlatformName, SPOTIFY_ACCESS_SCOPE
from CaseBonita.Services.ManagementLayer.PlaylistsManager import PlaylistsDbManagement
from CaseBonita.Services.PlaylistUploader.Handlers.Consts import CLIENT_ID, CLIENT_SECRET
from CaseBonita.Utils.RequestUtils import retry_request


class SpotifyUploadHandler():
    def __init__(self, user_name, _platform=PlatformName.SPOTIFY):
        self.user_name = user_name
        self.spotify = self.get_access_to_user()

    # development only
    LOCAL_SERVER = 'http://0.0.0.0:7000/'

    access_token = None

    def get_access_to_user(self):
        """
        This method uses spotipy's client to connect to a user.
        """
        token = util.prompt_for_user_token(
            client_secret=CLIENT_SECRET,
            client_id=CLIENT_ID,
            username=self.user_name,
            scope=SPOTIFY_ACCESS_SCOPE,
            redirect_uri='http://0.0.0.0:7000/'
        )
        if token:
            self.spotify = Spotify(auth=token)
            return self.spotify

    def get_tracks_id(self, song):
        artist = song[0]
        track = song[1]
        track_id = self.spotify.search(q=ARTIST + artist + TRACK + track, type=TRACK)
        return track_id

    def get_playlist_tracks(self, playlist_url):
        playlist = PlaylistsDbManagement.find_playlist(playlist_url=playlist_url)
        tracks_id = [self.get_tracks_id(song) for song in playlist]
        return tracks_id

    @retry_request(total_retries=4)
    def insert_new_playlist(self, playlist_name):
        """
        Inserts a new playlist at the user's account.
        """
        print(self.user_name)
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

    def write_songs_to_playlist(self, songs_id):
        """
        This method initiates the insert new playlist and takes the given name from it.
        it then lists all the tracks ids and uploads them to the playlist.
        """

        playlist, playlist_name = self.insert_new_playlist(playlist_name='yo')
        print(playlist_name)
        try:
            upload_songs_to_playlist = self.spotify.user_playlist_add_tracks(user=self.user_name,
                                                                             tracks=songs_id,
                                                                             playlist_id=self.get_playlist_id(
                                                                                 playlist_name)
                                                                             )
            return upload_songs_to_playlist
        except ConnectionError as e:
            print(e)

    def run(self, username, playlist_name, playlist_url):
        handler = SpotifyUploadHandler(user_name=username)
        handler.get_access_to_user()
        handler.insert_new_playlist(playlist_name=playlist_name)
        handler.get_playlist_id(playlist_name=playlist_name)
        handler.write_songs_to_playlist(songs_id=self.get_playlist_tracks(playlist_url=playlist_url))


if __name__ == '__main__':
    username = 'oa7fxnn3xwxveug6000igp0v6'
    songs_id = ['7xGfFoTpQ2E7fRF5lN10tr']
    source_url = "https://music.apple.com/il/playlist/shiras-18th-birthday/pl.u-9N9L24LIx3DZ3K0"
    handler = SpotifyUploadHandler(user_name=username)
    handler.run(username=username,
                playlist_name='yo',
                playlist_url=source_url)
