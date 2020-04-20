from spotipy import SpotifyOAuth, Spotify
import asyncio
from CaseBonita.Data.Consts import TITLE, ARTIST, TRACK
from CaseBonita.Services.PlaylistUploader.Handlers.Consts import CLIENT_SECRET, CLIENT_ID, LOCAL_SERVER, SCOPE


class ExtraDataFetcher:

    def add_tracks_ids(self, playlist):
        for track in playlist:
            track_id = self.async_get_tracks(track)
            di = {track[TITLE]: track_id}
            yield di

    def async_get_tracks(self, track):
        sp = Spotify()
        track = sp.search(q=f'{ARTIST}:' + track[ARTIST] + f'{TITLE}:' + track[TITLE], type=TRACK)
        print(track)
        return track

    def connect_spotify_api(self):
        """
        This method uses spotipy's client to connect to a user.
        """
        auth = SpotifyOAuth(client_secret=CLIENT_SECRET,
                            client_id=CLIENT_ID,
                            username="215zrdwn4rukc72ovlawttsta",
                            scope=SCOPE,
                            redirect_uri=LOCAL_SERVER
                            )
        return auth