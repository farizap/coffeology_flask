from blueprints import db
from flask_restful import fields
from datetime import datetime


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    historyID = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    photo = db.Column(db.String(250), nullable=False)

    responseFields = {
        'id': fields.Integer,
        'userID': fields.Integer,
        'recipeID': fields.Integer,
        'historyID': fields.Integer,
        'content': fields.String,
        'rating': fields.Integer,
        'createdAt': fields.DateTime,
        'photo': fields.String,
    }

    def __init__(self, userID, recipeID, historyID, content, rating, photo):
        self.userID = userID
        self.recipeID = recipeID
        self.historyID = historyID
        self.content = content
        self.rating = rating
        self.photo = photo
