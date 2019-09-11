from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Methods
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_methods = Blueprint('methods', __name__)
api = Api(bp_methods)


class MethodsResource(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        methodsQry = Methods.query

        methods = []
        for method in methodsQry.limit(data['rp']).offset(offset).all():
            methods.append(marshal(method, Methods.responseFields))
        if methods == []:
            pass
        else:
            return {'code': 200,
                    'message': 'oke',
                    'data': methods}, 200, {'Content-Type': 'application/json'}


api.add_resource(MethodsResource, '')
