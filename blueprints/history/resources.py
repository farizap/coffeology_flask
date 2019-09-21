from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import History
from blueprints.recipe.model import Recipes
from blueprints.step.model import Steps
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import ast
import math

bp_history = Blueprint('history', __name__)
api = Api(bp_history)


class HistoryListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @non_internal_required
    def get(self):
        """
        Get history by userID from token

        :param userID: the id of user
        :type userID: int, required
        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :param sort: sort query ascending or descending
        :type sort: string, optional
        :>json int pageNow: Page Now 
        :>json int pageTotal: Total page from query
        :>json array histories: contain recipes that users has used
        :status 200: success get recipes
        """
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        histories = History.query.filter_by(userID=claims['id'])

        histories = histories.order_by(desc(History.id))

        if data['sort'] == 'desc':
            histories = histories.order_by(desc(History.id))
        elif data['sort'] == 'asc':
            histories = histories.order_by((History.id))

        recipes = Recipes.query

        historyList = []
        for history in histories.limit(data['rp']).offset(offset).all():
            recipeID = history.recipeID
            recipe = recipes.get(recipeID)
            recipe.createdAt = history.createdAt
            historyList.append(marshal(recipe, Recipes.responseFields))

        pageTotal = math.ceil(histories.count() / data['rp'])

        return {
            'code': 200,
            'message': 'oke',
            'pageTotal': pageTotal,
            'pageNow': data['p'],
            'data': historyList
        }, 200


class HistoryResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @non_internal_required
    def post(self):
        """
        Post new history when user finished tutorial

        :param userID: from token
        :type userID: int, required
        :<json int recipeID: id from recipe user just used 
        :>json dict history: history response field: id, recipeID, userID, createdAt
        :status 201: success create data
        """
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('recipeID', location='json', required=True)
        data = parser.parse_args()

        history = History(claims['id'], data['recipeID'])

        db.session.add(history)

        db.session.commit()

        app.logger.debug('DEBUG : %s', history)

        # add brewCount
        recipe = Recipes.query.get(data['recipeID'])
        recipeBrewCount = marshal(recipe, Recipes.responseFields)['brewCount']

        recipe.brewCount = recipeBrewCount + 1
        db.session.commit()

        return {
            'code': 201,
            'message': 'oke',
            'data': marshal(history, History.responseFields)
        }, 201

    @jwt_required
    @internal_required
    def put(self, id):
        """
        Edit history, admin required

        :<json int userID: id of user that use the recipe
        :<json int recipeID: id of recipe user had used
        :>json dict history: history
        :status 200: success edit data
        :status 204: history not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('userID', location='json', required=True)
        parser.add_argument('recipeID', location='json', required=True)
        data = parser.parse_args()

        history = History.query.get(id)

        if history is None:
            return {'code': 404, 'message': 'History Not Found'}, 404

        history.userID = data['userID']
        history.recipeID = data['recipeID']
        db.session.commit()

        return {
            'code': 200,
            'message': 'oke',
            'data': marshal(history, History.responseFields)
        }, 200

    @jwt_required
    @internal_required
    def delete(self, id):
        """
        Delete history data, admin required

        :param id: id of history data
        :type id: int, required
        :status 200: success delete data
        :status 404: history not found
        """
        history = History.query.get(id)
        if history is None:
            return {'code': 404, 'message': 'History Not Found'}, 404

        db.session.delete(history)
        db.session.commit()

        return {'code': 200, 'message': 'History Deleted'}, 200


api.add_resource(HistoryListResource, '')
api.add_resource(HistoryResource, '', '/<id>')
