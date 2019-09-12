from blueprints import db
from flask_restful import fields
from datetime import datetime


class Recipes(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    methodID = db.Column(db.Integer, nullable=False)
    beanID = db.Column(db.Integer, nullable=False)
    beanName = db.Column(db.String(30), nullable=False)
    beanProcess = db.Column(db.String(30), nullable=False)
    beanRoasting = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)
    favoriteCount = db.Column(db.Integer, nullable=False, default=0)
    difficulty = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)

    responseFields = {
        'id': fields.Integer,
        'userID': fields.Integer,
        'name': fields.String,
        'methodID': fields.Integer,
        'beanID': fields.Integer,
        'beanName': fields.String,
        'beanProcess': fields.String,
        'beanRoasting': fields.String,
        'rating': fields.Float,
        'favoriteCount': fields.Integer,
        'difficulty': fields.Integer,
        'createdAt': fields.DateTime
    }

    def __init__(self, userID, name, methodID, beanID, beanName, beanProcess,
                 beanRoasting, rating, favoriteCount, difficulty):
        self.userID = userID
        self.name = name
        self.methodID = methodID
        self.beanID = beanID
        self.beanName = beanName
        self.beanProcess = beanProcess
        self.beanRoasting = beanRoasting
        self.rating = rating
        self.favoriteCount = favoriteCount
        self.difficulty = difficulty
