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

    def delete(self, id):
        userQry = Users.query.get(id)
        if userQry is None:
            return {'code': 404, 'status': 'User Not Found'}, 404

        db.session.delete(userQry)
        db.session.commit()

        return {'code': 200, 'message': 'User Deleted'}, 200


class UserListResource(Resource):

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

        userQry = Users.query

        users = []
        for user in userQry.limit(data['rp']).offset(offset).all():
            users.append(
                marshal(user, Users.responseFieldsJwt))

        if users == []:
            return {'code': 404, 'message': 'User Not Found'}, 404
        else:
            return {'code': 200, 'message': 'oke', 'data': users}, 200


api.add_resource(UserListResource, '')
api.add_resource(UserResource, '', '/<id>')
