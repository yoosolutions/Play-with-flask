import unittest, os
from app import app, db
from app.models import User

class UserCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        user1 = User(id = '1', username = 'Konstantin', email = 'k.tagintsev@gmail.com')
        user2 = User(id = '2', username = 'Ivan', email = 'test@mail.ru')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testPasswordHashing(self):
        user = User.query.get('1')
        user.set_password('test')
        self.assertFalse(user.check_password('lal'))
        self.assertTrue(user.check_password('test'))