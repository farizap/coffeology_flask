from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.recipeDetail.model import RecipeDetails
from blueprints import app, db, nonInternalRequired
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_recipeDetails = Blueprint('recipeDetails', __name__)
api = Api(bp_recipeDetails)


class RecipeDetailsListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        """
        Get list of recipeDetails

        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :param recipeID: filter by id of a recipe
        :type recipeID: int, optional
        :>json array recipeDetails: array cointaining list of recipeDetails
                                    that match the query
        :status 200: success get data of recipeDetails
        :status 404: recipeDetails not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('recipeID', type=int, location='args')
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        recipeDetailQry = RecipeDetails.query

        # to filter by recipeID
        if data['recipeID'] is not None:
            recipeDetailQry = recipeDetailQry.filter_by(
                recipeID=data['recipeID'])

        recipeDetails = []
        for recipe in recipeDetailQry.limit(data['rp']).offset(offset).all():
            recipeDetails.append(marshal(recipe, RecipeDetails.responseFields))

        if recipeDetails == []:
            return {'code': 404, 'message': 'RecipeDetail Not Found'}, 404
        else:
            return {'code': 200, 'message': 'oke', 'data': recipeDetails}, 200


api.add_resource(RecipeDetailsListResource, '')
