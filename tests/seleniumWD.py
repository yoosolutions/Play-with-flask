#To run the Selenium tests, you need to have the flask app running in TestingConfig.
import unittest, os, sys
sys.path.append('../')
from config import Config, TestConfig
Config.SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
from app import app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class UserCase(unittest.TestCase):
    def setUp(self):
        service = Service(executable_path=r'chromedriver.exe')
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')  # Run Chrome in headless mode.
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service = service, options = chrome_options)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.driver.get('http://127.0.0.1:5000')
        user1 = User(username = 'Konstantin', email = 'k.tagintsev@gmail.com')
        user2 = User(username = 'Ivan', email = 'test@mail.ru')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def testPasswordHashing(self):
        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)
        user1.set_password('test')
        self.assertFalse(user1.check_password('lal'))
        self.assertTrue(user1.check_password('test'))
        self.assertTrue(user2.username == 'Ivan')

