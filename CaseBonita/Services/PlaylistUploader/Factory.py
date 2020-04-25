from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Services.PlaylistUploader.Handlers.Spotify import SpotifyUploadHandler


class UploaderFactory(object):
    handlers = {
        PlatformName.SPOTIFY: SpotifyUploadHandler,
    }

    @classmethod
    def get_handler(cls, platform_name):
        return cls.handlers.get(platform_name)
