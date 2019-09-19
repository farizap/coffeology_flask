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
    if re.match(r"^[A-Za-z\s]+$", name):
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
        parser.add_argument('photo', location='json', default="")
        parser.add_argument('bio', location='json', default="")
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

        # dataBio = data['bio'].strip()
        # if dataBio == "":
        #     return {'code': 400, 'message': 'Bio is not valid'}, 400

        # password hashing
        passwordHash = hashlib.md5(dataPassword.encode())

        user = Users(dataEmail.lower(), passwordHash.hexdigest(), dataName,
                     data['photo'], data['bio'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return {
            'code': 201,
            'message': 'created',
            'data': marshal(user, Users.responseFieldsJwt)
        }, 201

    @jwt_required
    @non_internal_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json')
        parser.add_argument('passwordOld',location='json')
        parser.add_argument('passwordNew',location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('brewCount', type=int, location='json')
        parser.add_argument('recipeCount', type=int, location='json')
        parser.add_argument('photo', location='json')
        parser.add_argument('bio', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        userQry = Users.query.get(claims['id'])
        if userQry is None:
            return {'code': 404, 'message': 'User Not Found'}, 404

        # check if passwordOld match
        if args['passwordOld'] is not None:
            passwordOld = args['passwordOld'].strip()        
            passwordOldHash = hashlib.md5(passwordOld.encode())
            if passwordOldHash.hexdigest() != userQry.password:
                return {'code': 400, 'message': 'Wrong Password'}, 400

        # validation email
        if args['email'] is not None:
            dataEmail = args['email'].strip()
            dataEmail = dataEmail.lower()
            if isValidEmail(dataEmail) is False:
                return {'code': 400, 'message': 'Email is not valid'}, 400
            # check if email has been used
            emailHasUsed = Users.query.filter_by(email=dataEmail).first()
            if emailHasUsed is not None:
                return {'code': 400, 'message': 'Email has been used'}, 400

        # validation password
        if args['passwordNew'] and args['passwordOld'] is not None:
            dataPassword = args['passwordNew'].strip()
            if isValidPassword(dataPassword) is False:
                return {'code': 400, 'message': 'New Password is not valid'}, 400

        # validation name
        if args['name'] is not None:
            dataName = args['name'].strip()
            if isValidName(dataName) is False:
                return {'code': 400, 'message': 'Name is not valid'}, 400

        # validation bio
        if args['bio'] is not None:
            dataBio = args['bio'].strip()
            if dataBio == "":
                return {'code': 400, 'message': 'Bio is not valid'}, 400

        # if all validation complete, input data to database
        if args['email'] is not None:
            userQry.email = dataEmail
        if args['passwordNew'] is not None:
            passwordHash = hashlib.md5(dataPassword.encode())
            userQry.password = passwordHash.hexdigest()
        if args['name'] is not None:
            userQry.name = dataName
        if args['brewCount'] is not None:
            userQry.brewCount = args['brewCount']
        if args['recipeCount'] is not None:
            userQry.recipeCount = args['recipeCount']
        if args['photo'] is not None:
            userQry.photo = args['photo']
        if args['bio'] is not None:
            userQry.bio = dataBio

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


class UserMeResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @non_internal_required
    def get(self):
        claims = get_jwt_claims()
        user = Users.query.get(claims['id'])

        return {
            'code': 200,
            'message': 'oke',
            'data': marshal(user, Users.responseFieldsJwt)}, 200
            

class UserListAdminResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    @jwt_required
    @internal_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        data=parser.parse_args()

        offset=(data['p'] * data['rp']) - data['rp']

        userQry=Users.query

        users=[]
        for user in userQry.limit(data['rp']).offset(offset).all():
            users.append(marshal(user, Users.responseFieldsJwt))

        return {'code': 200, 'message': 'oke', 'data': users}, 200

api.add_resource(UserListAdminResource, '/admin')
api.add_resource(UserResource, '', '/<id>')
api.add_resource(UserMeResource, '/me')