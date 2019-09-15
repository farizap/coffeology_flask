from blueprints import db
from flask_restful import fields
from datetime import datetime


class Recipes(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    methodID = db.Column(db.Integer, nullable=False)
    originID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    beanName = db.Column(db.String(30), nullable=False)
    beanProcess = db.Column(db.String(30), nullable=False)
    beanRoasting = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0)
    favoriteCount = db.Column(db.Integer, nullable=False, default=0)
    reviewCount = db.Column(db.Integer, nullable=False, default=0)
    brewCount = db.Column(db.Integer, nullable=False, default=0)
    difficulty = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    time = db.Column(db.Integer, nullable=False)
    coffeeWeight = db.Column(db.Integer, nullable=False)
    water = db.Column(db.Integer, nullable=False)

    responseFields = {
        'id': fields.Integer,
        'userID': fields.Integer,
        'methodID': fields.Integer,
        'originID': fields.Integer,
        'name': fields.String,
        'beanName': fields.String,
        'beanProcess': fields.String,
        'beanRoasting': fields.String,
        'rating': fields.Float,
        'favoriteCount': fields.Integer,
        'reviewCount': fields.Integer,
        'brewCount': fields.Integer,
        'difficulty': fields.Integer,
        'createdAt': fields.DateTime,
        'time': fields.Integer,
        'coffeeWeight': fields.Integer,
        'water': fields.Integer,
    }

    def __init__(self, userID, name, methodID, originID, beanName, beanProcess,
                 beanRoasting, difficulty, time, coffeeWeight, water):
        self.userID = userID
        self.name = name
        self.methodID = methodID
        self.originID = originID
        self.beanName = beanName
        self.beanProcess = beanProcess
        self.beanRoasting = beanRoasting
        self.difficulty = difficulty
        self.time = time
        self.coffeeWeight = coffeeWeight
        self.water = water
