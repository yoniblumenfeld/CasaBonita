from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Services.PlaylistUploader.Handlers.Spotify import SpotifyUploaderHandler


class UploaderFactory(object):
    handlers = {
        PlatformName.SPOTIFY: SpotifyUploaderHandler,
    }

    @classmethod
    def get_handler(cls, platform_name):
        return cls.handlers.get(platform_name)
