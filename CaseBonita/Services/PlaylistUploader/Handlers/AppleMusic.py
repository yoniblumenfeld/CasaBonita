from selenium.webdriver.common.keys import Keys

from CaseBonita.Services.PlaylistUploader.Handlers.Base import BaseUploaderHandler
from CaseBonita.Services.PlaylistUploader.Handlers.consts import APPLEMUSIC_LOGIN_PAGE


class AppleMusicUploader(BaseUploaderHandler):

    def __init__(self, developer_key, _platform, _songs_json_file, user_credentials):
        super(BaseUploaderHandler, self).__init__(developer_key, _platform, _songs_json_file, user_credentials)

    def connect_to_user(self):
        self.driver.get(APPLEMUSIC_LOGIN_PAGE)
        assert "Python" in self.driver.title

        elem = self.driver.find_element_by_id("apple-music-authorize")
        elem.send_keys(Keys.RETURN)

        email, password = self.user_credentials['email'], self.user_credentials['password']
        enter_email = self.driver.find_element_by_class_name(
            "force-ltr form-textbox form-textbox-text lower-border-reset")
        enter_email.send_keys(f"{email}")
        enter_email.send_keys(Keys.RETURN)

        enter_password = self.driver.find_element_by_id("password_text_field")
        enter_password.send_keys(f"{password}")
        enter_password.send_keys(Keys.RETURN)

    def create_playlist(self):
        pass

    def write_songs_to_playlist(self):
        pass

    def check_all_songs_was_inserted(self):
        pass
