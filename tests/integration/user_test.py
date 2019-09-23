import json
from .. import app, client, cache, createTokenNonInternal
from .. import createTokenInternal, resetDatabase


class TestUserCrud():

    resetDatabase()
    user_id = 0

    # user get by id
    def testUserGetByIDValid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users/1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserGetByIDInvalid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users/-1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# user get all

    def testUserGetAllValid(self, client):
        token = createTokenInternal()
        res = client.get('/users/admin',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# user get by token

    def testUserGetByTokenValid(self, client):
        token = createTokenNonInternal()
        res = client.get('/users/me',
                         headers={'Authorization': 'Bearer ' + token},
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
            'photo': 'photo1',
            "bio": "bio"
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestUserCrud.user_id = res_json['data']['id']
        assert res.status_code == 201

    def testUserPostInvalidEmailHasBeenUsed(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba@coba.com',
            'password': 'Password',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidEmailTooShort(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'c@c.c',
            'password': 'Password',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidWrongEmailType(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'cccc.cccc',
            'password': 'Password',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidWrongPassword(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba1@coba.com',
            'password': 'password',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPostInvalidWrongName(self, client):
        # token = create_token_non_internal()
        data = {
            'email': 'coba1@coba.com',
            'password': 'Password1',
            'name': 'n4me',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# user put

    def testUserPutValid(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'user1@user.com',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'name',
            'brewCount': 1,
            'recipeCount': 1,
            "bio": "bio",
            'photo': 'photo1'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserPutInvalidEmailHasBeenUsed(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'admin@admin.com',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidEmailTooShort(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'c@c.c',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidWrongEmailType(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'cccc.cccc',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidWrongPassword(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'coba1@coba.com',
            'passwordOld': 'Password123',
            'passwordNew': 'Password1',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidWrongNewPasswordType(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'coba1@coba.com',
            'passwordOld': 'Password1',
            'passwordNew': 'Password',
            'name': 'name',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidWrongBio(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'coba1@coba.com',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'name',
            "bio": "       ",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testUserPutInvalidWrongName(self, client):
        token = createTokenNonInternal()
        data = {
            'email': 'coba1@coba.com',
            'passwordOld': 'Password1',
            'passwordNew': 'Password1',
            'name': 'n4me',
            "bio": "bio",
            'photo': 'photo'
        }
        res = client.put('/users',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# user delete by id

    def testUserDeleteValid(self, client):
        # token = create_token_non_internal()
        res = client.delete(f'/users/{TestUserCrud.user_id}',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserDeleteInvalidID(self, client):
        # token = create_token_non_internal()
        res = client.delete('/users/-1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404


# user options

    def testUserOptionsByIDValid(self, client):
        # token = create_token_non_internal()
        res = client.options('/users/1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserOptionsValid(self, client):
        # token = create_token_non_internal()
        res = client.options('/users', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserMeOptionsValid(self, client):
        res = client.options('/users/me', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testUserAdminOptionsValid(self, client):
        res = client.options('/users/admin', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

        # recipe delete by user
    def testRecipeUserDeleteValid(self, client):
        token = createTokenNonInternal()
        res = client.delete('/recipes/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeUserDeleteInvalid(self, client):
        token = createTokenNonInternal()
        res = client.delete('/recipes/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404
