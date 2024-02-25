import unittest, os, sys, HtmlTestRunner
sys.path.append('../')
from config import Config, TestConfig
Config.SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
from app import app, db
from app.models import User

class UserCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        user1 = User(username = 'Konstantin', email = 'k.tagintsev@gmail.com')
        user2 = User(username = 'Ivan', email = 'test@mail.ru')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testPasswordHashing(self):
        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)
        user1.set_password('test')
        self.assertFalse(user1.check_password('lal'))
        self.assertTrue(user1.check_password('test'))
        self.assertTrue(user2.username == 'Ivan')

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='HTMLTestRunner'))