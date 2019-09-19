import json
from . import app, client, cache, createTokenNonInternal
from . import createTokenInternal, resetDatabase


class TestAuthCrud():

    resetDatabase()
    Auth_id = 0

# auth valid
    def testAuthPostValid(self, client):
        data = {
            'email': 'user2@user.com',
            'password': 'Password1'
        }
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
        data = {
            'email': 'user2@user9.com',
            'password': 'Password1'
        }
        res = client.post('/token',
                        data=json.dumps(data),
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidWrongPassword(self, client):
        data = {
            'email': 'user2@user.com',
            'password': 'passWord1'
        }
        res = client.post('/token',
                        data=json.dumps(data),
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 401

    def testAuthPostInvalidEmail(self, client):
        data = {
            'email': 'user2user9.com',
            'password': 'Password1'
        }
        res = client.post('/token',
                        data=json.dumps(data),
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidEmailTooShort(self, client):
        data = {
            'email': 'u',
            'password': 'Password1'
        }
        res = client.post('/token',
                        data=json.dumps(data),
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testAuthPostInvalidPassword(self, client):
        data = {
            'email': 'user2@user9.com',
            'password': 'Passwordjh'
        }
        res = client.post('/token',
                        data=json.dumps(data),
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

#     # Auth get by id
#     def testAuthGetByIDValid(self, client):
#         # token = create_token_non_internal()
#         res = client.get('/token/1', content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def testAuthGetByIDInvalid(self, client):
#         # token = create_token_non_internal()
#         res = client.get('/token/-1', content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 404

# # Auth get all

#     def testAuthGetAllValid(self, client):
#         # token = create_token_non_internal()
#         res = client.get('/token', content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 200

# # Auth post

#     def testAuthPostValid(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba@coba.com',
#             'password': 'Password1',
#             'name': 'name',
#             'photo': 'photo1'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         TestAuthCrud.Auth_id = res_json['data']['id']
#         assert res.status_code == 201

#     def testAuthPostInvalidEmailHasBeenUsed(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba@coba.com',
#             'password': 'Password',
#             'name': 'name',
#             'photo': 'photo'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def testAuthPostInvalidEmailTooShort(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'c@c.c',
#             'password': 'Password',
#             'name': 'name',
#             'photo': 'photo'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def testAuthPostInvalidWrongEmailType(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'cccc.cccc',
#             'password': 'Password',
#             'name': 'name',
#             'photo': 'photo'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def testAuthPostInvalidWrongPassword(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba1@coba.com',
#             'password': 'password',
#             'name': 'name',
#             'photo': 'photo'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     def testAuthPostInvalidWrongName(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba1@coba.com',
#             'password': 'Password1',
#             'name': 'n4me',
#             'photo': 'photo'
#         }
#         res = client.post('/token',
#                           data=json.dumps(data),
#                           content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 400

# # Auth put

#     def testAuthPutValid(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba@coba.com',
#             'password': 'password1',
#             'name': 'name',
#             'brewCount': 1,
#             'recipeCount': 1,
#             'photo': 'photo1'
#         }
#         res = client.put(f'/token/{TestAuthCrud.Auth_id}',
#                          data=json.dumps(data),
#                          content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def testAuthPutInvalidID(self, client):
#         # token = create_token_non_internal()
#         data = {
#             'email': 'coba@coba.com',
#             'password': 'password1',
#             'name': 'name',
#             'brewCount': 1,
#             'recipeCount': 1,
#             'photo': 'photo1'
#         }
#         res = client.put('/token/-1',
#                          data=json.dumps(data),
#                          content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 404

# # Auth delete by id

#     def testAuthDeleteValid(self, client):
#         # token = create_token_non_internal()
#         res = client.delete('/token/1', content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     def testAuthDeleteInvalidID(self, client):
#         # token = create_token_non_internal()
#         res = client.delete('/token/-1', content_type='application/json')

#         res_json = json.loads(res.data)
#         assert res.status_code == 404


# Auth options


    def testAuthOptionsRefreshValid(self, client):
        res = client.options('/token/refresh', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testAuthOptionsValid(self, client):
        res = client.options('/token', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
