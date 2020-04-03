import bs4
import requests


class BaseDownloaderHandler(object):
    def __init__(self, source_url, source_platform):
        self.source_url = source_url
        self.source_platform = source_platform


class ScraperBaseDownloaderHandler(BaseDownloaderHandler):
    def __init__(self,source_url, source_platform):
        super(ScraperBaseDownloaderHandler, self).__init__(source_url, source_platform)
        self._parsing_engine = bs4.BeautifulSoup()

    def download_playlist(self):
        page = self._download_webpage(self.source_url)
        songs_and_artists_json = self._read_songs_and_artists(page)
        return songs_and_artists_json

    @classmethod
    def _download_webpage(cls, source_url):
        page = requests.get(source_url)
        return page

    @classmethod
    def _read_songs_and_artists(cls, web_page):
        """
        :param requests.Response web_page:
        :rtype:
        """
        raise NotImplementedError


class APIBaseDownloaderHandler(BaseDownloaderHandler):
    def download_playlist(self):
        raise NotImplementedError