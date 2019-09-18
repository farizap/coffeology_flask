from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from .model import Reviews
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.recipe.model import Recipes
from blueprints.user.model import Users

bp_reviews = Blueprint ('reviews',__name__)
api = Api(bp_reviews)

class ReviewResource(Resource):

    def __init__(self):
        pass

    def options (self, id=None):
        return {'code': 200, 'message': 'oke'}, 200


    def get (self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('recipeID', type=int, location='args', default=1)
        data = parser.parse_args()

        offset = (data['p']*data['rp']) - data['rp']

        reviews = Reviews.query

        # to filter by recipeID
        if data['recipeID'] is not None:
            reviews = reviews.filter_by(recipeID=data['recipeID'])

        reviews.order_by(Reviews.createdAt)

        reviewList = []
        for review in reviews.limit(data['rp']).offset(offset).all():
            reviewDict = marshal(review,Reviews.responseFields)
            if reviewDict['content'] != "":
                reviewDict['user'] = marshal(Users.query.get(review.userID),Users.responseFieldsJwt)
                reviewList.append(reviewDict)
       
        return {'code': 200, 'message': 'oke', 'data': reviewList}, 200

    @jwt_required
    @non_internal_required
    def post (self):
        parser = reqparse.RequestParser()
        parser.add_argument('recipeID', location='json', required=True)
        parser.add_argument('historyID', location='json', required=True)
        parser.add_argument('content', location='json',  required=False)
        parser.add_argument('rating', location='json', required=True)
        parser.add_argument('photo', location='json',  required=False)
        
        data = parser.parse_args()

        # get claims
        claims = get_jwt_claims()

        # add dataReview to reviews model
        review = Reviews(claims['id'], data['recipeID'],  data['historyID'], data['content'],  data['rating'], data['photo'])
        db.session.add(review)
        db.session.commit()

        app.logger.debug('DEBUG : %s', review)

         # add reviewCount
        recipe = Recipes.query.get(data['recipeID'])
        recipeReviewCount = int(marshal(recipe, Recipes.responseFields)['reviewCount'])
        recipeRating = int(marshal(recipe, Recipes.responseFields)['rating'])

        recipe.reviewCount = recipeReviewCount + 1
        recipe.rating = ((recipeRating*recipeReviewCount) + int(data['rating']))/(recipeReviewCount+ 1)
        db.session.commit()


        return {'code': 201, 'message': 'oke', 'data': marshal(review,Reviews.responseFields)}, 201

    @jwt_required
    @internal_required
    def put (self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('content', location='json',  required=False)
        parser.add_argument('rating', location='json', required=False)
        parser.add_argument('photo', location='json',  required=False)
        data = parser.parse_args()

        review = Reviews.query.get(id)

        # check review is valid
        if review is None:
            return {'code': 404, 'message': 'Review Not Found'}, 404

        # update review content
        if  data['content'] is not None:
            review.content = data['content']

        # update review rating
        if  data['rating'] is not None:
            review.content = data['rating']

        # update review photo
        if  data['photo'] is not None:
            review.content = data['photo']
       
        db.session.commit()

        return {'code': 200, 'message': 'Review updated'}, 200

    @jwt_required
    @internal_required
    def delete (self,id):
        review = Reviews.query.get(id)

        # check review is valid
        if review is None:
            return {'code': 404, 'message': 'Review Not Found'}, 404

        # delete review
        db.session.delete(review)
        db.session.commit()

        return {'code': 200, 'message': 'Review deleted'}, 200
            


api.add_resource(ReviewResource, '', '/<id>')