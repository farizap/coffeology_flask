import json
from . import app, client, cache, createTokenNonInternal, createTokenInternal, resetDatabase

class TestReviewCrud():

    resetDatabase()

    # method post
    def testReviewPostValid(self, client):
        token = createTokenNonInternal()
        data = {
            'recipeID': 1,
            'historyID': 1,
            'content': 'good',
            'rating': 1,
            'photo': 'a'
        }
        res = client.post('/reviews', data=json.dumps(data), headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 201

    # method get
    def testReviewGetByRecipeIDValid(self, client):
        token = createTokenNonInternal()
        data = {
            'recipeID': 1
        }
        res = client.get('/reviews', query_string=data, headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    # method put
    def testReviewPutByIDValid(self, client):
        token = createTokenInternal()
        data = {
            'content': 'good',
            'rating': 5,
            'photo': 'a'
        }
        res = client.put('/reviews/1',data=json.dumps(data), headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testReviewPutByIDInvalid(self, client):
        token = createTokenInternal()
        data = {
            'content': 'good',
            'rating': 5,
            'photo': 'a'
        }
        res = client.put('/reviews/2',data=json.dumps(data), headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404


    # method delete
    def testReviewDeleteByIDValid(self, client):
        token = createTokenInternal()
        res = client.delete('/reviews/1', headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testReviewDeleteByIDInvalid(self, client):
        token = createTokenInternal()
        res = client.delete('/reviews/2', headers={'Authorization':'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    # method options
    def testReviewOptionsByIDValid(self, client):
        res = client.options('/reviews/1',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
