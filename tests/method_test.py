import json
from . import app, client, cache, createTokenNonInternal
from . import createTokenInternal, resetDatabase


class TestMethodCrud():

    resetDatabase()
    client_id = 0

# method get
    def testMethodGetAllValid(self, client):
        # token = create_token_non_internal()
        res = client.get('/methods',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# method options
    def testMethodOptionsByIDValid(self, client):
        # token = create_token_non_internal()
        res = client.options('/methods',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
