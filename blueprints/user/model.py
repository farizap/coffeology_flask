from blueprints import db
from flask_restful import fields


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    brewCount = db.Column(db.Integer, nullable=False, default=0)
    recipeCount = db.Column(db.Integer, nullable=False, default=0)
    photo = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(250), nullable=True)

    responseFieldsDetails = {
        'id': fields.Integer,
        'email': fields.String,
        'password': fields.String,
        'name': fields.String,
        'brewCount': fields.Integer,
        'recipeCount': fields.Integer,
        'photo': fields.String,
        'status': fields.Integer,
        'role': fields.Integer,
        'bio': fields.String
    }

    responseFieldsJwt = {
        'id': fields.Integer,
        'email': fields.String,
        'name': fields.String,
        'brewCount': fields.Integer,
        'recipeCount': fields.Integer,
        'photo': fields.String,
        'status': fields.Integer,
        'role': fields.Integer,
        'bio': fields.String
    }

    def __init__(self, email, password, name, photo, bio):
        self.email = email
        self.password = password
        self.name = name
        self.photo = photo
        self.status = 1
        self.role = 0
        self.bio = bio