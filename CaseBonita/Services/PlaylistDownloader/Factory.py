from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Services.PlaylistDownloader.Handlers.AppleMusic import AppleMusicDownloaderHandler
from CaseBonita.Services.PlaylistDownloader.Handlers.Spotify import SpotifyDownloaderHandler


class DownloaderFactory(object):
    handlers = {
        PlatformName.SPOTIFY: SpotifyDownloaderHandler,
        PlatformName.APPLE_MUSIC: AppleMusicDownloaderHandler
    }

    @classmethod
    def get_handler(cls, platform_name):
        return cls.handlers.get(platform_name)
