import json
from . import app, client, cache, create_token_non_internal
from . import create_token_internal, reset_database


class TestRecipeDetailCrud():

    reset_database()

# recipeDetail get all
    def test_recipeDetail_get_all_valid_1(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipedetails', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipeDetail_get_all_valid_2(self, client):
        # token = create_token_non_internal()
        data = {
            'recipeID': 1
        }
        res = client.get('/recipedetails', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipeDetail_get_all_valid_3(self, client):
        # token = create_token_non_internal()
        data = {
            'recipeID': -1
        }
        res = client.get('/recipedetails', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# recipeDetail options

    def test_recipeDetail_options_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/recipedetails',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
