from blueprints import db
from tests import app, client, cache

from blueprints.user.resources import isValidEmail, isValidPassword, isValidName
from blueprints import auth


class TestUnit():
    # check email valid or not in auth resources
    def test_auth_isValidEmail(self, client):
        assert auth.isValidEmail('user1@user.com') == True
        assert auth.isValidEmail('user.com') == False

    def test_auth_isValidPassword(self, client):
        assert auth.isValidPassword('zxcV123') == True
        assert auth.isValidPassword('zxcv') == False

    def test_user_isValidEmail(self, client):
        assert isValidEmail('user1@user.com') == True
        assert isValidEmail('user.com') == False

    def test_user_isValidPassword(self, client):
        assert isValidPassword('zxcV123') == True
        assert isValidPassword('zxcv') == False

    def test_user_isValidName(self, client):
        assert isValidName('Fariz Nada Ade') == True
        assert isValidName('zxcv1') == False
