from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Steps
from sqlalchemy import desc
from blueprints import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_steps = Blueprint('steps', __name__)
api = Api(bp_steps)


class StepListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        """Get list of Steps in recipe by id recipeID

        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :param recipeID: filter by id of a recipe
        :type recipeID: int, required
        :>json array steps: array cointaining list of steps that match recipeID
        :status 200: success get data of steps
        :status 404: steps not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('recipeID', type=int, location='args', default=1)
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        stepQry = Steps.query

        # to filter by receipeID
        if data['recipeID'] is not None:
            stepQry = stepQry.filter_by(recipeID=data['recipeID'])

        stepQry.order_by(Steps.stepNumber)

        steps = []
        for step in stepQry.limit(data['rp']).offset(offset).all():
            steps.append(marshal(step, Steps.responseFields))
        if steps == []:
            return {'code': 404, 'message': 'Step Not Found'}, 404
        else:
            return {'code': 200, 'message': 'oke', 'data': steps}, 200


api.add_resource(StepListResource, '')
