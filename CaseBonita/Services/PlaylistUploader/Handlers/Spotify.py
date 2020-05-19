from CaseBonita.Data.Consts import ID, PlatformName
from CaseBonita.Data.TestCases import SpotifyTestCase, AppleMusicTestCase
from CaseBonita.Utils.Platforms.Spotify.SpotfiyAccess import SpotifyConnector
from CaseBonita.Utils.RequestUtils import retry_request


class SpotifyUploadHandler(SpotifyConnector):
    def __init__(self, user_name, _platform=PlatformName.SPOTIFY):
        self.user_name = user_name
        self.spotify = self.return_auth_client(self.user_name)

    # development only
    LOCAL_SERVER = 'http://0.0.0.0:7000/'
    access_token = None

    @retry_request(total_retries=4)
    def insert_new_playlist(self, playlist_name):
        """
        Inserts a new playlist at the user's account.
        """
        playlist = self.spotify.user_playlist_create(user=self.user_name, name=playlist_name)
        return playlist

    def get_created_playlist_id(self, playlist_name):
        playlist = self.insert_new_playlist(playlist_name=playlist_name)
        playlist_id = playlist[ID]
        return playlist_id

    def write_songs_to_playlist(self, songs_id, playlist_name):
        """
        This method initiates the insert new playlist and takes the given name from it.
        it then lists all the tracks ids and uploads them to the playlist.
        """

        playlist_id = self.get_created_playlist_id(playlist_name=playlist_name)
        try:
            upload_songs_to_playlist = self.spotify.user_playlist_add_tracks(user=self.user_name,
                                                                             tracks=songs_id,
                                                                             playlist_id=playlist_id
                                                                             )
            print(f'{playlist_name} Was inserted successfully')
        except ConnectionError as e:
            print(e)

    def run(self, playlist_name, playlist_url):
        handler = SpotifyUploadHandler(user_name=self.user_name)
        handler.insert_new_playlist(playlist_name=playlist_name)
        handler.get_playlist_id(playlist_name=playlist_name)
        handler.write_songs_to_playlist(songs_id=SpotifyTestCase.SONGS_ID_LIST, playlist_name=playlist_name)


if __name__ == '__main__':
    handler = SpotifyUploadHandler(user_name=SpotifyTestCase.USERNAME)
    handler.run(playlist_url=AppleMusicTestCase.PLAYLIST_EXAMPLE, playlist_name='yo')
