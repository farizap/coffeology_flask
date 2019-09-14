from blueprints import db
from flask_restful import fields
from datetime import datetime


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)

    responseFields = {
        'id': fields.Integer,
        'userID': fields.Integer,
        'recipeID': fields.Integer,
        'createdAt': fields.DateTime
    }

    def __init__(self, userID, recipeID):
        self.userID = userID
        self.recipeID = recipeID
