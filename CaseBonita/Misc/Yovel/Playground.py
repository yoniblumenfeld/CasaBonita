from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from CaseBonita.Data.Consts import APPLEMUSIC_LOGIN_PAGE, CHROMEDRIVER


class AppleMusicUploader:

    def __init__(self, user):
        self.user = user
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER)

    def connect_to_user(self):
        self.driver.get(APPLEMUSIC_LOGIN_PAGE)
        try:
            # Let's get passed this shit, then move on to the password field.
            self.wait_for_load('account_name_text_field')
            apple_id = self.driver.find_element_by_id('account_name_text_field')
            apple_id.send_keys(self.user['email'])
        except:
            print('seriously, kyle, fuck you')

        password = self.driver.find_element_by_id('password_text_field')
        password.send_keys(self.user['password'])
        self.driver.find_element_by_id(
            "sign-in").click()

    def wait_for_load(self, element_id):
        timeout = 5  # 5 second time out on loading
        element_present = EC.presence_of_element_located((By.ID, element_id))
        WebDriverWait(self.driver, timeout).until(element_present)

    def create_playlist(self):
        pass

    def write_songs_to_playlist(self):
        pass

    def check_all_songs_was_inserted(self):
        pass


if __name__ == '__main__':
    user = {'email': 'yovell04@gmail.com',
            'password': 'Yovelcohen1'}
    a = AppleMusicUploader(user=user, )
    a.connect_to_user()
