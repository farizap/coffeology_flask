import json
from . import app, client, cache, create_token_non_internal
from . import create_token_internal, reset_database


class TestUserCrud():

    reset_database()
    user_id = 0

# user get by id
    def testUserGetByIDValid(self, client): 
        # token = create_token_non_internal()
        res = client.get('/users/1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserGetByIDInvalid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users/-1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# user get all
    def testUserGetAllValid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# user post
    def testUserPostValid(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba@coba.com',
            'password': 'Password1',
            'name': 'name',
            'photo': 'photo1'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestUserCrud.user_id = res_json['data']['id']
        assert res.status_code == 200

    def testUserPostInvalidEmailHasBeenUsed(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba@coba.com',
            'password': 'Password',
            'name': 'name',
            'photo': 'photo'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidEmailTooShort(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'c@c.c',
            'password': 'Password',
            'name': 'name',
            'photo': 'photo'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidWrongEmailType(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'cccc.cccc',
            'password': 'Password',
            'name': 'name',
            'photo': 'photo'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    def testUserPostInvalidWrongPassword(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba1@coba.com',
            'password': 'password',
            'name': 'name',
            'photo': 'photo'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidWrongName(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba1@coba.com',
            'password': 'Password1',
            'name': 'n4me',
            'photo': 'photo'
        }
        res = client.post('/users', data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# user put
    def test_user_put_valid(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba@coba.com',
            'password': 'password1',
            'name': 'name',
            'brewCount': 1,
            'recipeCount': 1,
            'photo': 'photo1'
        }
        res = client.put(f'/users/{TestUserCrud.user_id}',
                         data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_put_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba@coba.com',
            'password': 'password1',
            'name': 'name',
            'brewCount': 1,
            'recipeCount': 1,
            'photo': 'photo1'
        }
        res = client.put('/users/-1', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# user delete by id
    def test_user_delete_valid(self, client):
        # token = create_token_non_internal()
        res = client.delete('/users/1',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_delete_invalid(self, client):
        # token = create_token_non_internal()
        res = client.delete('/users/-1',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# user options
    def test_user_options_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/users/1',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_options_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/users',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
