from selenium import webdriver

from CaseBonita.Services.PlaylistUploader.Handlers.consts import CHROMEDRIVER


class BaseUploaderHandler:
    def __init__(self, developer_key, _platform, _songs_json_file, user_credentials):
        self.developer_key = developer_key
        self.platform = _platform
        self.songs_json_file = _songs_json_file
        self.user_credentials = user_credentials
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER)

    def connect_to_user(self, *args, **kwargs):
        """
        Use of kw/args is due to every platform may require different parameters to connect.
        """
        pass

    def create_playlist(self):
        raise NotImplementedError

    def write_songs_to_playlist(self):
        raise NotImplementedError

    def check_all_songs_was_inserted(self):
        """
        Uses the Playlist Downloader Handler to get the newly created Playlist and check it matches the
        self.songs_json_file.
        """
        raise NotImplementedError


class BaseSelniumUploader(BaseUploaderHandler):
    """
    If a Platform doesn't have a suitable API with upload playlist feature (Those Apple Bitches).
    Use a Selenium WebDriver to connect to the user's account and create a playlist.
    """

    def __init__(self, _songs_json_file, user_credentials, _platform, driver):
        super(BaseUploaderHandler, self).__init__(_songs_json_file, user_credentials, _platform, driver)

    def connect_to_user(self):
        pass

    def create_playlist(self):
        pass


class BaseAPIUploader(BaseUploaderHandler):
    """
    Base Class to upload songs via the Platform's API.
    """

    def __init__(self, _songs_json_file, user_credentials, _platform):
        super(BaseUploaderHandler, self).__init__(_songs_json_file, user_credentials, _platform)

    def create_developer_credentials(self):
        pass

    def create_playlist(self, **kwargs):
        """
        Implementation depends as at least the spotipy lib allows us to create a new playlist without the need to
        separate creation and writing.
        """
        pass
