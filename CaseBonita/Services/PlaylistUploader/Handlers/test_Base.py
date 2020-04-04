import unittest
from unittest import TestCase

from selenium import webdriver

from CaseBonita.Services.PlaylistUploader.Handlers.consts import CHROMEDRIVER


class TestAppleMusicUploader(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER)

    def test_connect_to_platform(self):
        pass

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
