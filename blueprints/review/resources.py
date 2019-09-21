from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from blueprints.review.model import Reviews
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.recipe.model import Recipes
from blueprints.user.model import Users
import math

bp_reviews = Blueprint('reviews', __name__)
api = Api(bp_reviews)


class ReviewResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        """Get list of review

        :param p: Page number
        :type p: int, optional
        :param rp: Number of entries per page
        :type rp: int, optional
        :param recipeID: filter by id of a recipe
        :type recipeID: int, optional
        :>json array review: array cointaining list of review that match the query
        :status 200: success get data of review
        :status 404: review not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('recipeID', type=int, location='args', default=1)
        data = parser.parse_args()

        offset = (data['p'] * data['rp']) - data['rp']

        reviews = Reviews.query

        # to filter by recipeID
        if data['recipeID'] is not None:
            reviews = reviews.filter_by(recipeID=data['recipeID'])

        reviews.order_by(Reviews.createdAt)

        reviewList = []
        for review in reviews.limit(data['rp']).offset(offset).all():
            reviewDict = marshal(review, Reviews.responseFields)
            if reviewDict['content'] != "":
                reviewDict['user'] = marshal(Users.query.get(review.userID),
                                             Users.responseFieldsJwt)
                reviewList.append(reviewDict)

        pageTotal = math.ceil(reviews.count() / data['rp'])

        return {
            'code': 200,
            'message': 'oke',
            'pageTotal': pageTotal,
            'pageNow': data['p'],
            'data': reviewList
        }, 200

    @jwt_required
    @non_internal_required
    def post(self):
        """Post new review user submitted after running a coffee guide

        :reqheader Accept: application/json
        :<json int recipeID: id of the recipe that reviewed
        :<json int historyID: id of the history related to the review
        :<json string content: review user submitted in review form
        :<json int rating: rating user given to the recipe
        :<json string photo: url of photo taken by user after brew coffee
        :status 201: review created
        """
        parser = reqparse.RequestParser()
        parser.add_argument('recipeID', location='json', required=True)
        parser.add_argument('historyID', location='json', required=True)
        parser.add_argument('content', location='json', required=False)
        parser.add_argument('rating', location='json', required=True)
        parser.add_argument('photo', location='json', required=False)

        data = parser.parse_args()

        # get claims
        claims = get_jwt_claims()

        # add dataReview to reviews model
        review = Reviews(claims['id'], data['recipeID'], data['historyID'],
                         data['content'], data['rating'], data['photo'])
        db.session.add(review)
        db.session.commit()

        app.logger.debug('DEBUG : %s', review)

        # add reviewCount
        recipe = Recipes.query.get(data['recipeID'])
        recipeReviewCount = int(
            marshal(recipe, Recipes.responseFields)['reviewCount'])
        recipeRating = int(marshal(recipe, Recipes.responseFields)['rating'])

        recipe.reviewCount = recipeReviewCount + 1
        recipe.rating = ((recipeRating * recipeReviewCount) +
                         int(data['rating'])) / (recipeReviewCount + 1)
        db.session.commit()

        return {
            'code': 201,
            'message': 'oke',
            'data': marshal(review, Reviews.responseFields)
        }, 201

    @jwt_required
    @internal_required
    def put(self, id):
        """Edit review, admin required

        :<json string content: review user submitted in review form
        :<json int rating: rating user given to the recipe
        :<json string photo: url of photo taken by user after brew coffee
        :status 200: success edit data
        :status 204: review not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('content', location='json', required=False)
        parser.add_argument('rating', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)
        data = parser.parse_args()

        review = Reviews.query.get(id)

        # check review is valid
        if review is None:
            return {'code': 404, 'message': 'Review Not Found'}, 404

        # update review content
        if data['content'] is not None:
            review.content = data['content']

        # update review rating
        if data['rating'] is not None:
            review.content = data['rating']

        # update review photo
        if data['photo'] is not None:
            review.content = data['photo']

        db.session.commit()

        return {'code': 200, 'message': 'Review updated'}, 200

    @jwt_required
    @internal_required
    def delete(self, id):
        """Delete review data, admin required
        
        :param id: id of review data
        :type id: int, required
        :status 200: success delete data
        :status 404: review not found
        """
        review = Reviews.query.get(id)

        # check review is valid
        if review is None:
            return {'code': 404, 'message': 'Review Not Found'}, 404

        # delete review
        db.session.delete(review)
        db.session.commit()

        return {'code': 200, 'message': 'Review deleted'}, 200


api.add_resource(ReviewResource, '', '/<id>')