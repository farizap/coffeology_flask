from blueprints import db
from flask_restful import fields


class Methods(db.Model):
    __tablename__ = "methods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    responseFields = {
        'id': fields.Integer,
        'name': fields.String,
        'icon': fields.String,
        'difficulty': fields.Integer
    }

    def __init__(self, name, icon, difficulty):
        self.name = name
        self.icon = icon
        self.difficulty = difficulty
