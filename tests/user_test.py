import json
from . import app, client, cache, create_token_non_internal
from . import create_token_internal, reset_database


class TestUserCrud():

    reset_database()
    client_id = 0

# user get by id
    def test_user_get_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users/1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_get__by_id_invalid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users/-1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# user get by id
    def test_user_get_all_valid(self, client):
        # token = create_token_non_internal()
        res = client.get('/users',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

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
