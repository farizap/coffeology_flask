from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import History
from blueprints.recipe.model import Recipes
from blueprints.step.model import Steps
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import ast

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
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
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
        return {'code': 200, 'message': 'oke', 'data': historyList}, 200

class HistoryResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @non_internal_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('recipeID', location='json', required=True)
        data = parser.parse_args()

        history = History(claims['id'], data['recipeID'])

        db.session.add(history)
        db.session.commit()

        app.logger.debug('DEBUG : %s', history)

        return {
            'code': 201,
            'message': 'oke',
            'data': marshal(history, History.responseFields)
        }, 201

    @jwt_required
    @internal_required
    def put(self, id):
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
        history = History.query.get(id)
        if history is None:
            return {'code': 404, 'message': 'History Not Found'}, 404

        db.session.delete(history)
        db.session.commit()

        return {
            'code': 200,
            'message': 'History Deleted'
        }, 200


api.add_resource(HistoryListResource, '')
api.add_resource(HistoryResource, '', '/<id>')
