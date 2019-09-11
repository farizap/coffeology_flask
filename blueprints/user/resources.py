from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_users = Blueprint('users', __name__)
api = Api(bp_users)


class UserResource(Resource):

    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        userQry = Users.query.get(id)
        if userQry is not None:
            return {'code': 200, 'message': 'oke',
                    'data': marshal(userQry, Users.responseFieldsJwt)}
        return {'code': 404, 'message': 'User Not Found'}, 404


api.add_resource(UserResource, '', '/<id>')
