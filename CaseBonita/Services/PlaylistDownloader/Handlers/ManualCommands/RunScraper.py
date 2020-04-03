from CaseBonita.Data.Consts import PlatformName
from CaseBonita.Services.PlaylistDownloader import Factory

if __name__ == '__main__':
    source_url = "https://music.apple.com/il/playlist/shiras-18th-birthday/pl.u-9N9L24LIx3DZ3K0"
    source_platform = PlatformName.APPLE_MUSIC
    handler = Factory.DownloaderFactory.get_handler(source_platform)
    handler(source_url, source_platform).download_playlist()