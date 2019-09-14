from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marsal
from .model import Reviews
from blueprints import app, db, internal_required non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_reviews = Blueprint ('reviews',__name__)
api = Api(bp_reviews)

class ReviewResource(Resource):

    def __init__(self):
        pass

    def option (self):
        return {'code': 200, 'message': 'oke'}, 200

    def get (self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args' default=25)
        parser.add_argument('recipeID', type=int, location='args', default=1)
        data = parser.parse_args()