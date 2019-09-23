import json
from .. import app, client, cache, createTokenNonInternal
from .. import createTokenInternal, resetDatabase


class TestRecipeDetailCrud():

    resetDatabase()

    # recipeDetail get all
    def testRecipeDetailGetAllValid_1(self, client):
        res = client.get('/recipedetails', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeDetailGetAllByRecipeIDValid(self, client):
        data = {'recipeID': 1}
        res = client.get('/recipedetails',
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeDetailGetAllByRecipeIDInvalid(self, client):
        data = {'recipeID': -1}
        res = client.get('/recipedetails',
                         query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    # recipeDetail options
    def testRecipeDetailOptionsValid(self, client):
        res = client.options('/recipedetails', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
