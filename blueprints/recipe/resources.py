from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Recipes
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_recipes = Blueprint('recipes', __name__)
api = Api(bp_recipes)


class RecipesResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        RecipeQry = Recipes.query.get(id)
        if RecipeQry is not None:
            return {'code': 200, 'message': 'oke',
                    'data': marshal(RecipeQry, Recipes.responseFields)}, 200
        return {'code': 404, 'message': 'Recipe Not Found'}, 404


class RecipesListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('userID', type=int, location='args')
        parser.add_argument('methodID', type=int, location='args')
        parser.add_argument('orderby', location='args',
                            choices=('favoriteCount', 'difficulty'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        recipeQry = Recipes.query

        # to filter by userID or methodID
        if data['userID'] is not None:
            recipeQry = recipeQry.filter_by(userID=data['userID'])
        if data['methodID'] is not None:
            recipeQry = recipeQry.filter_by(methodID=data['methodID'])

        # to handle orderby difficulty or favouriteCount
        if data['orderby'] is not None:
            if data['orderby'] == 'favoriteCount':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.favoriteCount))
                else:
                    recipeQry = recipeQry.order_by((Recipes.favoriteCount))
            elif data['orderby'] == 'difficulty':
                if data['sort'] == 'desc':
                    recipeQry = recipeQry.order_by(desc(Recipes.difficulty))
                else:
                    recipeQry = recipeQry.order_by((Recipes.difficulty))

        recipes = []
        for recipe in recipeQry.limit(data['rp']).offset(offset).all():
            recipes.append(marshal(recipe, Recipes.responseFields))

        if recipes == []:
            return {'code': 404, 'message': 'Recipe Not Found'}, 404
        else:
            return {'code': 200, 'message': 'oke', 'data': recipes}, 200


api.add_resource(RecipesListResource, '')
api.add_resource(RecipesResource, '', '/<id>')
