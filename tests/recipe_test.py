import json
from . import app, client, cache, create_token_non_internal
from . import create_token_internal, reset_database


class TestRecipeCrud():

    reset_database()

# recipe get by id
    def test_recipe_get_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes/1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_by_id_invalid(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes/-1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# recipe get all
    def test_recipe_get_all_valid_1(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_valid_2(self, client):
        # token = create_token_non_internal()
        data = {
            'userID': 1,
            'methodID': 1,
            'orderby': 'favoriteCount',
            'sort': 'asc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_valid_3(self, client):
        # token = create_token_non_internal()
        data = {
            'userID': 1,
            'methodID': 1,
            'orderby': 'favoriteCount',
            'sort': 'desc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_valid_4(self, client):
        # token = create_token_non_internal()
        data = {
            'orderby': 'difficulty',
            'sort': 'asc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_valid_5(self, client):
        # token = create_token_non_internal()
        data = {
            'orderby': 'difficulty',
            'sort': 'desc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            'userID': -1,
            'methodID': -1
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

# recipe post

    def test_recipe_post_valid(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_post_data_recipe_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": " ",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_recipeDetails_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": " "
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_step_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "  ",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_step_empty(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_recipe_not_integer(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": "methodID",
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_recipeDetail_not_integer(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": 1,
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": "aroma",
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_recipe_post_data_step_not_integer(self, client):
        # token = create_token_non_internal()
        data = {
            "recipes":{
                "name": "name",
                "methodID": "methodID",
                "beanID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1
            },
            "recipeDetails":{
                "recipeID": 1,
                "fragrance": 1,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note"
            },
            "steps":[
                {
                "recipeID": 1,
                "stepNumber": 1,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": 2,
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                },
                {
                "recipeID": 1,
                "stepNumber": "stepNumber",
                "stepTypeID": 1,
                "note": "note",
                "time": 1,
                "amount": 1
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data),
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# recipe options

    def test_recipe_options_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/recipes/1',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_options_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/recipes',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
