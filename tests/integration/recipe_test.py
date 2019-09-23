import json
from .. import app, client, cache, createTokenNonInternal
from .. import createTokenInternal, resetDatabase


class TestRecipeCrud():

    resetDatabase()
    recipeID = 0

# recipe get by id
    def testRecipeGetByIDValid(self, client):
        # token = createTokenNonInternal()
        res = client.get('/recipes/1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetByIDInvalid(self, client):
        # token = createTokenNonInternal()
        res = client.get('/recipes/-1',
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404


# recipe get all


    def testRecipeGetAllValid(self, client):
        res = client.get('/recipes', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_1(self, client):
        data = {
            'userID': 1,
            'methodID': 1,
            'orderby': 'difficulty',
            'sort': 'asc',
            'search': 'name',
            'methods' : 1,
            'origins' : 1,
            'difficulties' : 1
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_2(self, client):
        data = {
            'userID': 1,
            'methodID': 1,
            'orderby': 'rating',
            'sort': 'desc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_2_1(self, client):
        data = {
            'userID': 1,
            'methodID': 1,
            'orderby': 'rating',
            'sort': 'asc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_3(self, client):
        data = {
            'orderby': 'difficulty',
            'sort': 'asc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_4(self, client):
        data = {
            'orderby': 'difficulty',
            'sort': 'desc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_5(self, client):
        data = {
            'orderby': 'brewCount',
            'sort': 'asc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeGetAllValidUsingParams_6(self, client):
        data = {
            'orderby': 'brewCount',
            'sort': 'desc'
        }
        res = client.get('/recipes', query_string=data,
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# recipe post

    def testRecipePostValid(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 201

    def testRecipePostInvalidDataRecipe(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": " ",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataRecipeDetail(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": " ",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataStep(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataStepEmpty(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": []
        }
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataRecipeNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": "methodID",
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataRecipeDetailNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataStepNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": "methodID",
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidWaterTemp(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": "salah"
            },
            "steps": [
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
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePostInvalidDataStepNotIntegerAmount(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
                    "amount": "salah"
                }
            ]
        }
        res = client.post('/recipes', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# recipe put

    def testRecipePutValid(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipePutInvalidRecipeID(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/2', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 403

    def testRecipePutInvalidDataRecipe(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": " ",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataRecipeDetail(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": " ",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataStep(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/2', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataStepEmpty(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": []
        }
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataRecipeNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": "methodID",
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataRecipeDetailNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataStepNotInteger(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": "methodID",
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
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
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidWaterTemp(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": "salah"
            },
            "steps": [
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
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

    def testRecipePutInvalidDataStepNotIntegerAmount(self, client):
        token = createTokenNonInternal()
        data = {
            "recipes": {
                "name": "name",
                "methodID": 1,
                "originID": 1,
                "beanName": "beanName",
                "beanProcess": "beanProcess",
                "beanRoasting": "beanRoasting",
                "difficulty": 1, "time": 40, "coffeeWeight": 17, "water": 200
            },
            "recipeDetails": {
                "recipeID": 1,
                "fragrance": 0.4,
                "aroma": 1,
                "cleanliness": 1,
                "sweetness": 1,
                "taste": 1,
                "acidity": 1,
                "aftertaste": 1,
                "balance": 1,
                "globalTaste": 1,
                "body": 1,
                "note": "note",
                "grindSize": 2,
                "waterTemp": 93
            },
            "steps": [
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
                    "amount": "salah"
                }
            ]
        }
        res = client.put('/recipes/1', data=json.dumps(data), headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 400

# recipe options

    def testRecipeOptionsByIDValid(self, client):
        res = client.options('/recipes/1',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeOptionsValid(self, client):
        res = client.options('/recipes',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def testRecipeUserOptionsValid(self, client):
        res = client.options('/recipes/user',
                             content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

# recipe user get by token
    def testRecipeUserGetValid(self, client):
        token = createTokenNonInternal()
        res = client.get('/recipes/user',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200


