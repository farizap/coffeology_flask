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


class RecipesResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
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

        db.session.commit()

        return {'code': 201, 'message': 'created'}, 201


class RecipesListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
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
        claims = get_jwt_claims()
        recipes = Recipes.query.filter_by(userID=claims['id'])

        recipeList = []
        for recipe in recipes.all():
            recipeList.append(marshal(recipe, Recipes.responseFields))
        return {'code': 200, 'message': 'oke', 'data': recipeList}, 200


api.add_resource(RecipesListResource, '')
api.add_resource(RecipesUserResource, '/user')
api.add_resource(RecipesResource, '', '/<id>')
