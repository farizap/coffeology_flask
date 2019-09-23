import json
from .. import app, client, cache, createTokenNonInternal
from .. import createTokenInternal, resetDatabase


class TestStepCrud():

    resetDatabase()

    # step get all
    def testStepGetAllValid(self, client):
        data = {'recipeID': 1}
        res = client.get('/steps',
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testStepGetAllInvalid(self, client):
        data = {'recipeID': -1}
        res = client.get('/steps',
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    # step options
    def testStepOptionsValid(self, client):
        res = client.options('/steps', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
