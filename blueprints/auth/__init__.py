from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.user.model import Users
from flask_cors import CORS
import re

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


def isValidEmail(email):
    # to validate email
    pattern = "^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,}$"
    if len(email) > 7:
        if re.match(pattern, email) is not None:
            return True
        return False
    else:
        return False


def isValidPassword(password):
    # to validate password minimum 6 characters, at least one capital and one number
    if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d]{6,30}$", password):
        return True
    else:
        return False


class CreateTokenResources(Resource):

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',
                            location='json', required=True)
        parser.add_argument('password',
                            location='json', required=True)
        args = parser.parse_args()

        if isValidEmail(args['email']) is False:
            return {'code': 400, 'message': 'Email is not valid'}, 400

        if isValidPassword(args['password']) is False:
            return {'code': 400, 'message': 'Password is not valid'}, 400

        userQry = Users.query

        userQry = userQry.filter_by(email=args['email'])
        userQry = userQry.filter_by(password=args['password']).first()

        if userQry is not None:
            user_data = marshal(userQry, Users.responseFieldsJwt)
            token = create_access_token(
                identity=args['email'], user_claims=user_data)
        else:
            return {'code': 401,
                    'message': 'UNATHORIZED invalid email or password'}, 401
        return {'code': 200, 'message': 'oke', 'data': token}, 200


class RefreshTokenResources(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        user_data = get_jwt_claims()
        token = create_access_token(
            identity=current_user, user_claims=user_data)
        return {'code': 200, 'message': 'oke', 'data': token}, 200


api.add_resource(CreateTokenResources, '')
api.add_resource(RefreshTokenResources, '/refresh')
