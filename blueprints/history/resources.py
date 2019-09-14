from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import History
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import ast

bp_history = Blueprint('history', __name__)
api = Api(bp_history)


class HistoryResource(Resource):

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

        historyQry = History.query.filter_by(userID=claims['id'])

        if data['sort'] == 'desc':
            historyQry = historyQry.order_by(desc(History.userID))
        elif data['sort'] == 'desc':
            historyQry = historyQry.order_by((History.userID))

        histories = []
        for history in historyQry.limit(data['rp']).offset(offset).all():
            histories.append(marshal(history, History.responseFields))
        return {'code': 200, 'message': 'oke', 'data': histories}, 200

    @jwt_required
    @non_internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('History', location='json')
        parser.add_argument('recipeDetails', location='json')
        parser.add_argument('steps', location='json')
        data = parser.parse_args()

        # convert string into dict or list
        dataHistoryDict = ast.literal_eval(data['History'])
        dataRecipeDetailsDict = ast.literal_eval(data['recipeDetails'])
        dataSteps = ast.literal_eval(data['steps'])

        # check all data's History is not null
        for key in dataHistoryDict:
            if type(dataHistoryDict[key]) == int:
                continue

            # to remove space at end
            dataHistoryDict[key] = dataHistoryDict[key].strip()
            if dataHistoryDict[key] == "":
                return {'code': 400,
                        'message': f'{key} tidak boleh kosong'}, 400

        # check all data's recipeDetails is not null
        for key in dataRecipeDetailsDict:
            if type(dataRecipeDetailsDict[key]) == int:
                continue

            # to remove space at end
            dataRecipeDetailsDict[key] = dataRecipeDetailsDict[key].strip()
            if dataRecipeDetailsDict[key] == "":
                return {'code': 400,
                        'message': f'{key} tidak boleh kosong'}, 400

        # check all data's steps is not null
        if dataSteps == []:
            return {'code': 400,
                    'message': 'Steps tidak boleh kosong'}, 400
        for stepDict in dataSteps:
            for key in stepDict:
                if type(stepDict[key]) == int:
                    continue

                stepDict[key] = stepDict[key].strip()  # to remove space at end
                if stepDict[key] == "":
                    return {'code': 400,
                            'message': f'{key} tidak boleh kosong'}, 400

        recipeDataInt = ['methodID', 'beanID', 'difficulty']

        # validate input data int for recipe
        for data in recipeDataInt:
            try:
                dataHistoryDict[data] = int(dataHistoryDict[data])
            except Exception as e:
                return {'code': 400, 'message': f'{data} harus integer'}, 400

        # validate input data int for recipeDetails
        for key in dataRecipeDetailsDict:
            if key != 'note':
                try:
                    dataRecipeDetailsDict[key] = int(
                        dataRecipeDetailsDict[key])
                except Exception as e:
                    return {'code': 400,
                            'message': f'{key} harus integer'}, 400

        # validate input data int for recipeDetails
        for stepDict in dataSteps:
            for key in stepDict:
                if key != 'note':
                    try:
                        stepDict[key] = int(stepDict[key])
                    except Exception as e:
                        return {'code': 400,
                                'message': f'{key} harus integer'}, 400


api.add_resource(HistoryResource, '')
