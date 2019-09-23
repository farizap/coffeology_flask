import json
from . import app, client, cache, createTokenNonInternal
from . import createTokenInternal, resetDatabase


class TestAuthCrud():

    resetDatabase()
    Auth_id = 0

    # auth valid
    def testAuthPostValid(self, client):
        data = {'email': 'user2@user.com', 'password': 'Password1'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testAuthPostRefreshValid_1(self, client):
        token = createTokenInternal()
        res = client.post('/token/refresh',
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testAuthPostRefreshValid_2(self, client):
        token = createTokenNonInternal()
        res = client.post('/token/refresh',
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    # auth not valid
    def testAuthPostInvalidEmailNotRegistered(self, client):
        data = {'email': 'user2@user9.com', 'password': 'Password1'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidWrongPassword(self, client):
        data = {'email': 'user2@user.com', 'password': 'passWord1'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 401

    def testAuthPostInvalidEmail(self, client):
        data = {'email': 'user2user9.com', 'password': 'Password1'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidEmailTooShort(self, client):
        data = {'email': 'u', 'password': 'Password1'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidPassword(self, client):
        data = {'email': 'user2@user9.com', 'password': 'Passwordjh'}
        res = client.post('/token',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthOptionsRefreshValid(self, client):
        res = client.options('/token/refresh', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testAuthOptionsValid(self, client):
        res = client.options('/token', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
