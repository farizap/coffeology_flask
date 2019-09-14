import json
from . import app, client, cache, createTokenNonInternal
from . import createTokenInternal, resetDatabase


class TestHistoryCrud():

    resetDatabase()
    historyID = 0

# history get all
    def testHistoryGetAll(self, client):
        token = createTokenNonInternal()
        res = client.get('/history',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testHistoryGetAllDesc(self, client):
        token = createTokenNonInternal()
        data = {
            "sort": "desc"
        }
        res = client.get('/history',
                         headers={'Authorization': 'Bearer ' + token},
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testHistoryGetAllAsc(self, client):
        token = createTokenNonInternal()
        data = {
            "sort": "asc"
        }
        res = client.get('/history',
                         headers={'Authorization': 'Bearer ' + token},
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# history post
    def testHistoryPostValid(self, client):
        token = createTokenNonInternal()
        data = {
            'recipeID': 1
        }
        res = client.post('/history', data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)

        TestHistoryCrud.historyID = res_json['data']['id']
        assert res.status_code == 201

    def testHistoryPostInvalidToken(self, client):
        token = createTokenInternal()
        data = {
            'recipeID': 1
        }
        res = client.post('/history', data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)

        TestHistoryCrud.historyID = res_json['data']['id']
        assert res.status_code == 403

    def testHistoryPostInvalidHasNotData(self, client):
        token = createTokenNonInternal()
        res = client.post('/history',
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# history put
    def testHistoryPutValid(self, client):
        token = createTokenInternal()
        data = {
            'userID': 1,
            'recipeID': 1
        }
        res = client.put(f'/history/{TestHistoryCrud.historyID}',
                         data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testHistoryPutInvalidID(self, client):
        token = createTokenInternal()
        data = {
            'userID': 1,
            'recipeID': 1
        }
        res = client.put('/history/-10000', data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def testHistoryPutInvalidToken(self, client):
        token = createTokenNonInternal()
        data = {
            'userID': 1,
            'recipeID': 1
        }
        res = client.put('/history/1', data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 403

# history delete by id
    def testHistoryDeleteValid(self, client):
        token = createTokenInternal()
        res = client.delete(f'/history/{TestHistoryCrud.historyID}',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testHistoryDeleteInvalidID(self, client):
        token = createTokenInternal()
        res = client.delete('/history/-1000',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def testHistoryDeleteInvalidToken(self, client):
        token = createTokenNonInternal()
        res = client.delete('/history/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 403

# history options
    def testHistoryOptionsByIDValid(self, client):
        res = client.options('/history/1',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testHistoryOptionsValid(self, client):
        res = client.options('/history',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
