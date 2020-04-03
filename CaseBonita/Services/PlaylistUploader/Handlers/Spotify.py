import spotipy

class SpotifyUploader:

    def __init__(self, service, name, user_id):
        self.service = service
        self.name = name
        self.user_id = user_id

    def _create_playlist(self, tracks=None):
        if tracks is None:
            tracks = []

        playlist = self.service.user_playlist_create(self.user_id,
                                                     self.name)
        self.service.user_playlist_replace_tracks(self.user_id,
                                                  playlist['id'], tracks)
