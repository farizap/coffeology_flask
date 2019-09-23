import json
from . import app, client, cache, createTokenNonInternal
from . import createTokenInternal, resetDatabase


class TestBeanCrud():

    resetDatabase()

    # step get all
    def testStepGetAllValid(self, client):
        res = client.get('/beans', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    # step get by id
    def testStepGetByIDValid(self, client):
        res = client.get('/beans/1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testStepGetByIDInvalid(self, client):
        res = client.get('/beans/-1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    # step options
    def testStepOptionsValidByID(self, client):
        res = client.options('/beans/1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testStepOptionsValid(self, client):
        res = client.options('/beans', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
