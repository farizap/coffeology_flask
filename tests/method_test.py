import json
from . import app, client, cache, create_token_non_internal
from . import create_token_internal, reset_database


class TestMethodCrud():

    reset_database()
    client_id = 0

# method get
    def test_method_get_all_valid(self, client):
        # token = create_token_non_internal()
        res = client.get('/methods',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# method options
    def test_method_options_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/methods',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
