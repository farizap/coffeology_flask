from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import re
import hashlib

bp_users = Blueprint('users', __name__)
api = Api(bp_users)


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
    # to validate password, at least one capital and one number
    if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d]{6,30}$", password):
        return True
    else:
        return False


def isValidName(name):
    # to validate name just alphabet
    if re.match(r"[A-Za-z]{2,25}( [A-Za-z]{2,25})?", name):
        return True
    return False


class UserResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        userQry = Users.query.get(id)
        if userQry is not None:
            return {
                'code': 200,
                'message': 'oke',
                'data': marshal(userQry, Users.responseFieldsJwt)
            }, 200
        return {'code': 404, 'message': 'User Not Found'}, 404

    def post(self):
        '''User register new account'''

        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('photo', location='json', required=True)
        data = parser.parse_args()

        dataEmail = data['email'].strip()
        if isValidEmail(dataEmail) is False:
            return {'code': 400, 'message': 'Email is not valid'}, 400

        # check if email has been used
        emailHasUsed = Users.query.filter_by(email=dataEmail).first()
        if emailHasUsed is not None:
            return {'code': 400, 'message': 'Email has been used'}, 400

        dataPassword = data['password'].strip()
        if isValidPassword(dataPassword) is False:
            return {'code': 400, 'message': 'Password is not valid'}, 400

        dataName = data['name'].strip()
        if isValidName(dataName) is False:
            return {'code': 400, 'message': 'Name is not valid'}, 400

        # password hashing
        passwordHash = hashlib.md5(dataPassword.encode())

        user = Users(dataEmail.lower(), passwordHash.hexdigest(), dataName,
                     data['photo'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return {
            'code': 201,
            'message': 'created',
            'data': marshal(user, Users.responseFieldsJwt)
        }, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json')
        parser.add_argument(
            'password',
            location='json',
        )
        parser.add_argument('name', location='json')
        parser.add_argument('brewCount', type=int, location='json')
        parser.add_argument('recipeCount', type=int, location='json')
        parser.add_argument('photo', location='json')
        args = parser.parse_args()

        userQry = Users.query.get(id)
        if userQry is None:
            return {'code': 404, 'message': 'User Not Found'}, 404

        if args['email'] is not None:
            userQry.email = args['email']
        if args['password'] is not None:
            userQry.password = args['password']
        if args['name'] is not None:
            userQry.name = args['name']
        if args['brewCount'] is not None:
            userQry.brewCount = args['brewCount']
        if args['recipeCount'] is not None:
            userQry.recipeCount = args['recipeCount']
        if args['photo'] is not None:
            userQry.photo = args['photo']

        db.session.commit()
        return {
            'code': 200,
            'message': 'oke',
            'data': marshal(userQry, Users.responseFieldsJwt)
        }, 200

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
            users.append(marshal(user, Users.responseFieldsJwt))

        return {'code': 200, 'message': 'oke', 'data': users}, 200


api.add_resource(UserListResource, '')
api.add_resource(UserResource, '', '/<id>')
