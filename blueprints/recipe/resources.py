from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import ast
import math
bp_recipes = Blueprint('recipes', __name__)
api = Api(bp_recipes)

# import model
from blueprints.recipe.model import Recipes
from blueprints.recipeDetail.model import RecipeDetails
from blueprints.step.model import Steps
from blueprints.user.model import Users
from blueprints.history.model import History
from blueprints.review.model import Reviews


class RecipesResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        """Return data about a recipes from 3 tables : Recipes, RecipeDetails, and Steps (filter by recipeID)

        :param id: The id of the wanted recipes
        :type id: int, required
        :query details: If it is passed, data recipe returned
        :status 200: Recipe is found and data returned returned
        :status 404: No recipe was found with this id
        """
        recipe = Recipes.query.get(id)

        if recipe is not None:
            recipeDetail = RecipeDetails.query.filter_by(
                recipeID=recipe.id).first()
            steps = Steps.query.filter_by(recipeID=recipe.id).all()
            user = Users.query.get(recipe.userID)

            # create response data
            resData = {}
            resData['recipe'] = marshal(recipe, Recipes.responseFields)
            resData['recipeDetails'] = marshal(recipeDetail,
                                               RecipeDetails.responseFields)
            resData['user'] = marshal(user, Users.responseFieldsJwt)

            stepList = []
            for step in steps:
                stepList.append(marshal(step, Steps.responseFields))

            resData['recipeSteps'] = stepList

            return {'code': 200, 'message': 'oke', 'data': resData}, 200
        return {'code': 404, 'message': 'Recipe Not Found'}, 404

    @jwt_required
    @non_internal_required
    def post(self):
        """Create new recipes

        :reqheader Accept: application/json
        :<json object recipes: recipe general info
        :<json object recipeDetails: recipe detail info
        :<json array steps: list of steps in the recipe
        :query details: If it is passed, data added to DB
        :status 201: Recipe created
        :status 400: Invalid user input 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('recipes', location='json')
        parser.add_argument('recipeDetails', location='json')
        parser.add_argument('steps', location='json')
        data = parser.parse_args()

        # convert string into dict or list
        dataRecipesDict = ast.literal_eval(data['recipes'])
        dataRecipeDetailsDict = ast.literal_eval(data['recipeDetails'])
        dataSteps = ast.literal_eval(data['steps'])

        # check all data's recipes is not null
        for key in dataRecipesDict:
            if type(dataRecipesDict[key]) == int:
                continue

            # to remove space at end
            dataRecipesDict[key] = dataRecipesDict[key].strip()
            if dataRecipesDict[key] == "":
                return {
                    'code': 400,
                    'message': f'{key} Resep tidak boleh kosong'
                }, 400

        # check all data's recipeDetails is not null
        for key in dataRecipeDetailsDict:
            if type(dataRecipeDetailsDict[key]) == float:
                continue
            if type(dataRecipeDetailsDict[key]) == int:
                continue
            # to remove space at end
            dataRecipeDetailsDict[key] = dataRecipeDetailsDict[key].strip()
            if dataRecipeDetailsDict[key] == "":
                return {
                    'code': 400,
                    'message': f'{key} Resep Detail tidak boleh kosong'
                }, 400

        # check all data's steps is not null
        if dataSteps == []:
            return {'code': 400, 'message': 'Steps tidak boleh kosong'}, 400
        for stepDict in dataSteps:
            for key in stepDict:
                if type(stepDict[key]) == int:
                    continue

                stepDict[key] = stepDict[key].strip()  # to remove space at end
                if stepDict[key] == "":
                    return {
                        'code': 400,
                        'message': f'{key} Step tidak boleh kosong'
                    }, 400

        recipeDataInt = ['methodID', 'originID', 'difficulty']

        # validate input data int for recipe
        for data in recipeDataInt:
            try:
                dataRecipesDict[data] = int(dataRecipesDict[data])
            except Exception as e:
                return {
                    'code': 400,
                    'message': f'{data} Resep harus integer'
                }, 400

        # validate input data int for recipeDetails
        for key in dataRecipeDetailsDict:

            if key != 'note':
                if key == 'waterTemp' or key == 'grindSize':
                    try:
                        dataRecipeDetailsDict[key] = int(
                            dataRecipeDetailsDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Resep Detail harus integer'
                        }, 400
                else:
                    try:
                        dataRecipeDetailsDict[key] = float(
                            dataRecipeDetailsDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Resep Detail harus float'
                        }, 400

        # validate input data int for recipeDetails
        for stepDict in dataSteps:
            for key in stepDict:
                if key != 'note':
                    try:
                        stepDict[key] = int(stepDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Step harus integer'
                        }, 400

        # get claims
        claims = get_jwt_claims()

        # add dataRecipesDict to recipes model
        recipe = Recipes(
            claims['id'], dataRecipesDict['name'], dataRecipesDict['methodID'],
            dataRecipesDict['originID'], dataRecipesDict['beanName'],
            dataRecipesDict['beanProcess'], dataRecipesDict['beanRoasting'],
            dataRecipesDict['difficulty'], dataRecipesDict['time'],
            dataRecipesDict['coffeeWeight'], dataRecipesDict['water'])

        db.session.add(recipe)
        db.session.commit()

        # add dataRecipeDetailsDict to RecipeDetails
        recipeDetail = RecipeDetails(
            recipe.id, dataRecipeDetailsDict['fragrance'],
            dataRecipeDetailsDict['aroma'],
            dataRecipeDetailsDict['cleanliness'],
            dataRecipeDetailsDict['sweetness'], dataRecipeDetailsDict['taste'],
            dataRecipeDetailsDict['acidity'],
            dataRecipeDetailsDict['aftertaste'],
            dataRecipeDetailsDict['balance'],
            dataRecipeDetailsDict['globalTaste'],
            dataRecipeDetailsDict['body'], dataRecipeDetailsDict['note'],
            dataRecipeDetailsDict['grindSize'],
            dataRecipeDetailsDict['waterTemp'])

        db.session.add(recipeDetail)

        # add dataSteps to Steps
        for stepNumber, dataStep in enumerate(dataSteps, 1):
            step = Steps(recipe.id, stepNumber, dataStep['stepTypeID'],
                         dataStep['note'], dataStep['time'],
                         dataStep['amount'])

            db.session.add(step)
        
        # add total recipeCount in data user
        user = Users.query.get(claims['id'])
        user.recipeCount += 1

        db.session.commit()

        return {'code': 201, 'message': 'created'}, 201

    @jwt_required
    @non_internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('recipes', location='json')
        parser.add_argument('recipeDetails', location='json')
        parser.add_argument('steps', location='json')
        data = parser.parse_args()

        # convert string into dict or list
        dataRecipesDict = ast.literal_eval(data['recipes'])
        dataRecipeDetailsDict = ast.literal_eval(data['recipeDetails'])
        dataSteps = ast.literal_eval(data['steps'])

        # check all data's recipes is not null
        for key in dataRecipesDict:
            if type(dataRecipesDict[key]) == int:
                continue

            # to remove space at end
            dataRecipesDict[key] = dataRecipesDict[key].strip()
            if dataRecipesDict[key] == "":
                return {
                    'code': 400,
                    'message': f'{key} Resep tidak boleh kosong'
                }, 400

        # check all data's recipeDetails is not null
        for key in dataRecipeDetailsDict:
            if type(dataRecipeDetailsDict[key]) == float:
                continue
            if type(dataRecipeDetailsDict[key]) == int:
                continue
            # to remove space at end
            dataRecipeDetailsDict[key] = dataRecipeDetailsDict[key].strip()
            if dataRecipeDetailsDict[key] == "":
                return {
                    'code': 400,
                    'message': f'{key} Resep Detail tidak boleh kosong'
                }, 400

        # check all data's steps is not null
        if dataSteps == []:
            return {'code': 400, 'message': 'Steps tidak boleh kosong'}, 400
        for stepDict in dataSteps:
            for key in stepDict:
                if type(stepDict[key]) == int:
                    continue

                stepDict[key] = stepDict[key].strip()  # to remove space at end
                if stepDict[key] == "":
                    return {
                        'code': 400,
                        'message': f'{key} Step tidak boleh kosong'
                    }, 400

        recipeDataInt = ['methodID', 'originID', 'difficulty']

        # validate input data int for recipe
        for data in recipeDataInt:
            try:
                dataRecipesDict[data] = int(dataRecipesDict[data])
            except Exception as e:
                return {
                    'code': 400,
                    'message': f'{data} Resep harus integer'
                }, 400

        # validate input data int for recipeDetails
        for key in dataRecipeDetailsDict:

            if key != 'note':
                if key == 'waterTemp' or key == 'grindSize':
                    try:
                        dataRecipeDetailsDict[key] = int(
                            dataRecipeDetailsDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Resep Detail harus integer'
                        }, 400
                else:
                    try:
                        dataRecipeDetailsDict[key] = float(
                            dataRecipeDetailsDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Resep Detail harus float'
                        }, 400

        # validate input data int for recipeDetails
        for stepDict in dataSteps:
            for key in stepDict:
                if key != 'note':
                    try:
                        stepDict[key] = int(stepDict[key])
                    except Exception as e:
                        return {
                            'code': 400,
                            'message': f'{key} Step harus integer'
                        }, 400

        # get claims
        claims = get_jwt_claims()
        recipe = Recipes.query.get(id)

        # validate userID in recipe
        if claims['id'] != recipe.userID:
            return {
                    'code': 400,
                    'message': "Anda Tidak Dapat Mengedit Resep Ini"
            }, 400

        # edit data recipe
        recipe.name = dataRecipesDict['name']
        recipe.methodID = dataRecipesDict['methodID']
        recipe.originID = dataRecipesDict['originID']
        recipe.beanName = dataRecipesDict['beanName']
        recipe.beanProcess = dataRecipesDict['beanProcess']
        recipe.beanRoasting = dataRecipesDict['beanRoasting']
        recipe.difficulty = dataRecipesDict['difficulty']
        recipe.time = dataRecipesDict['time']
        recipe.coffeeWeight = dataRecipesDict['coffeeWeight']
        recipe.water = dataRecipesDict['water']

        # edit data RecipeDetails
        recipeDetail = RecipeDetails.query.filter_by(recipeID=id).first()
        recipeDetail.fragrance = dataRecipeDetailsDict['fragrance']
        recipeDetail.aroma = dataRecipeDetailsDict['aroma']
        recipeDetail.cleanliness = dataRecipeDetailsDict['cleanliness']
        recipeDetail.sweetness = dataRecipeDetailsDict['sweetness']
        recipeDetail.taste = dataRecipeDetailsDict['taste']
        recipeDetail.acidity = dataRecipeDetailsDict['acidity']
        recipeDetail.aftertaste = dataRecipeDetailsDict['aftertaste']
        recipeDetail.balance = dataRecipeDetailsDict['balance']
        recipeDetail.globalTaste = dataRecipeDetailsDict['globalTaste']
        recipeDetail.body = dataRecipeDetailsDict['body']
        recipeDetail.note = dataRecipeDetailsDict['note']
        recipeDetail.grindSize = dataRecipeDetailsDict['grindSize']
        recipeDetail.waterTemp = dataRecipeDetailsDict['waterTemp']

        # edit data Steps
        stepsOld = Steps.query.filter_by(recipeID=id)
        for step in stepsOld:
            db.session.delete(step)

        for stepNumber, dataStep in enumerate(dataSteps, 1):
            step = Steps(recipe.id, stepNumber, dataStep['stepTypeID'],
                         dataStep['note'], dataStep['time'],
                         dataStep['amount'])

            db.session.add(step)

        db.session.commit()
        return {'code': 200, 'message': 'edited'}, 200

    @jwt_required
    @non_internal_required
    def delete(self, id):
        claims = get_jwt_claims()
        recipe = Recipes.query.get(id)
        if recipe is None:
            return {'code': 404, 'status': 'Recipe Not Found'}, 404

        if recipe.userID != claims['id']:
            return {'code': 404, 'status': 'Anda Tidak Dapat Menghapus Resep Ini'}, 404

        db.session.delete(recipe)

        # to remove total recipe in table user
        user = Users.query.get(claims['id'])
        user.recipeCount -= 1

        # delete recipe details
        recipeDetails = RecipeDetails.query.filter_by(recipeID=id).all()
        for recipeDetail in recipeDetails:
            db.session.delete(recipeDetail)

        # delete step
        steps = Steps.query.filter_by(recipeID=id).all()
        for step in steps:
            db.session.delete(step)
        
        # delete review
        reviews = Reviews.query.filter_by(recipeID=id).all()
        for review in reviews:
            db.session.delete(review)

        #delete history and brewCount in table user
        histories = History.query.filter_by(recipeID=id).all()
        for history in histories:
            user = Users.query.get(history.userID)
            user.brewCount -= 1
            db.session.delete(history)

        db.session.commit()
        return {'code': 200, 'message': 'Recipe Deleted'}, 200

class RecipesListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        """Get list of Recipes with optional params.

        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :param userID: filter by user who create the recipe
        :type userID: int, optional
        :param methodID: filter by method type
        :type methodID: int, optional
        :param orderby: order query by a column. i.e rating, difficulty, brewCount
        :type orderby: string, optional
        :param sort: sort query ascending or descending
        :type sort: string, optional
        :param methods: contain methods that user choose to filter
        :type methods: string, optional 
        :>json int pageNow: Page Now 
        :>json int pageTotal: Total page from query
        :>json dict recipes: dictionary that contains recipe general info
        :>json dict recipeDetails: dictionary that contains recipe detail info
        :>json array recipeSteps: array that contain dictionary of steps in the recipe     
        :status 200: success get data


        **Example response**:

        .. sourcecode:: http

          GET /recipes/user 
          Host: api.coffeology.shop
          Accept: application/json

          {
              "code": 200,
              "message": "oke",
              "pageTotal": 1,
              "pageNow": 1,
              "data": [
                  {
                      "id": 2,
                      "userID": 4,
                      "methodID": 1,
                      "originID": 3,
                      "name": "french press 14",
                      "beanName": "origin 3",
                      "beanProcess": "difficulty 2",
                      "beanRoasting": "beanRoasting",
                      "rating": 0.0,
                      "reviewCount": 0,
                      "brewCount": 0,
                      "difficulty": 2,
                      "createdAt": "Sat, 21 Sep 2019 15:35:00 -0000",
                      "time": 20,
                      "coffeeWeight": 16,
                      "water": 200
                   },
                  {
                      "id": 3,
                      "userID": 4,
                      "methodID": 1,
                      "originID": 3,
                      "name": "french press 14",
                      "beanName": "origin 3",
                      "beanProcess": "difficulty 2",
                      "beanRoasting": "beanRoasting",
                      "rating": 0.0,
                      "reviewCount": 0,
                      "brewCount": 0,
                      "difficulty": 2,
                      "createdAt": "Sat, 21 Sep 2019 15:35:01 -0000",
                      "time": 20,
                      "coffeeWeight": 16,
                      "water": 200
                   }
               ]
           }
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        parser.add_argument('userID', type=int, location='args')
        parser.add_argument('methodID', type=int, location='args')
        parser.add_argument('orderby',
                            location='args',
                            choices=('rating', 'difficulty', 'brewCount'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        # Fariz
        parser.add_argument('methods', location='args')
        parser.add_argument('search', location='args')
        parser.add_argument('origins', location='args')
        parser.add_argument('difficulties', location='args')

        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        recipeQry = Recipes.query
        recipeQry = recipeQry.order_by(desc(Recipes.id))

        # Fariz
        # filter by search
        if data['search'] is not None:
            recipeQry = recipeQry.filter(
                Recipes.name.like('%' + data['search'] + '%')
                | Recipes.beanName.like('%' + data['search'] + '%'))

        # filter by methods
        if data['methods'] is not None:
            methods = data['methods'].split(',')
            recipeQry = recipeQry.filter(Recipes.methodID.in_(methods))

        # filter by origins
        if data['origins'] is not None:
            origins = data['origins'].split(',')
            recipeQry = recipeQry.filter(Recipes.originID.in_(origins))

        # filter by difficulties
        if data['difficulties'] is not None:
            difficulties = data['difficulties'].split(',')
            recipeQry = recipeQry.filter(Recipes.difficulty.in_(difficulties))

        # to filter by userID or methodID
        if data['userID'] is not None:
            recipeQry = recipeQry.filter_by(userID=data['userID'])
        if data['methodID'] is not None:
            recipeQry = recipeQry.filter_by(methodID=data['methodID'])

        # to handle orderby difficulty or favouriteCount
        if data['orderby'] is not None:
            if data['orderby'] == 'rating':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.rating))
                else:
                    recipeQry = recipeQry.order_by((Recipes.rating))
            elif data['orderby'] == 'difficulty':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.difficulty))
                else:
                    recipeQry = recipeQry.order_by((Recipes.difficulty))
            elif data['orderby'] == 'brewCount':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.brewCount))
                else:
                    recipeQry = recipeQry.order_by((Recipes.brewCount))

        recipes = []
        for recipe in recipeQry.limit(data['rp']).offset(offset).all():
            recipes.append(marshal(recipe, Recipes.responseFields))
        pageTotal = math.ceil(recipeQry.count() / data['rp'])
        return {
            'code': 200,
            'message': 'oke',
            'pageTotal': pageTotal,
            'pageNow': data['p'],
            'recipes': recipes
        }, 200


class RecipesUserResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @non_internal_required
    def get(self):
        """Get recipe by userID from token

        :param userID: the id of user
        :type userID: int, required
        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :>json int pageNow: Page Now 
        :>json int pageTotal: Total page from query
        :>json array recipes: array that contains list of recipes
        :status 200: success get recipes

        **Example response**:

        .. sourcecode:: http

          GET /recipes/user 
          Host: api.coffeology.shop
          Accept: application/json

          {
              "code": 200,
              "message": "oke",
              "pageTotal": 1,
              "pageNow": 1,
              "data": [
                  {
                      "id": 2,
                      "userID": 4,
                      "methodID": 1,
                      "originID": 3,
                      "name": "french press 14",
                      "beanName": "origin 3",
                      "beanProcess": "difficulty 2",
                      "beanRoasting": "beanRoasting",
                      "rating": 0.0,
                      "reviewCount": 0,
                      "brewCount": 0,
                      "difficulty": 2,
                      "createdAt": "Sat, 21 Sep 2019 15:35:00 -0000",
                      "time": 20,
                      "coffeeWeight": 16,
                      "water": 200
                   },
                  {
                      "id": 3,
                      "userID": 4,
                      "methodID": 1,
                      "originID": 3,
                      "name": "french press 14",
                      "beanName": "origin 3",
                      "beanProcess": "difficulty 2",
                      "beanRoasting": "beanRoasting",
                      "rating": 0.0,
                      "reviewCount": 0,
                      "brewCount": 0,
                      "difficulty": 2,
                      "createdAt": "Sat, 21 Sep 2019 15:35:01 -0000",
                      "time": 20,
                      "coffeeWeight": 16,
                      "water": 200
                   }
               ]
           }

        """

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        data = parser.parse_args()

        claims = get_jwt_claims()

        recipes = Recipes.query.filter_by(userID=claims['id'])
        recipes = recipes.order_by(desc(Recipes.id))

        offset = (data['p'] * data['rp']) - data['rp']

        recipeList = []
        for recipe in recipes.limit(data['rp']).offset(offset).all():
            recipeList.append(marshal(recipe, Recipes.responseFields))

        pageTotal = math.ceil(recipes.count() / data['rp'])

        return {
            'code': 200,
            'message': 'oke',
            'pageTotal': pageTotal,
            'pageNow': data['p'],
            'data': recipeList
        }, 200


api.add_resource(RecipesListResource, '')
api.add_resource(RecipesUserResource, '/user')
api.add_resource(RecipesResource, '', '/<id>')
