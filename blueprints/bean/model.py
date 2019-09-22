from blueprints import db
from flask_restful import fields


class Beans(db.Model):
    __tablename__ = "beans"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    originID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    photo = db.Column(db.String(250), nullable=True, default="")
    fragrance = db.Column(db.Float, nullable=False)
    flavor = db.Column(db.Float, nullable=False)
    aftertaste = db.Column(db.Float, nullable=False)
    acidity = db.Column(db.Float, nullable=False)
    body = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    uniformity = db.Column(db.Float, nullable=False)
    cleanCups = db.Column(db.Float, nullable=False)
    sweetness = db.Column(db.Float, nullable=False)
    overall = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True,default="")
    cupping = db.Column(db.String(250), nullable=True,default="")
    advantage = db.Column(db.String(250), nullable=True,default="")
    disadvantage = db.Column(db.String(250), nullable=True,default="")
    location = db.Column(db.String(250), nullable=True,default="")

    responseFields = {
        'id': fields.Integer,
        'originID': fields.Integer,
        'name': fields.String,
        'photo': fields.String,
        'fragrance': fields.Float,
        'flavor': fields.Float,
        'aftertaste': fields.Float,
        'acidity': fields.Float,
        'body': fields.Float,
        'balance': fields.Float,
        'uniformity': fields.Float,
        'cleanCups': fields.Float,
        'sweetness': fields.Float,
        'overall': fields.Float,
        'description': fields.String,
        'cupping': fields.String,
        'advantage': fields.String,
        'disadvantage': fields.String,
        'location': fields.String,
    }

    responseFieldsGetAll = {
        'id': fields.Integer,
        'originID': fields.Integer,
        'name': fields.String
    }


    def __init__(self, originID, name, photo, fragrance, flavor, aftertaste, acidity, body, balance, uniformity, cleanCups, sweetness, 
                 overall, description, cupping,  advantage,
                 disadvantage, location):
        self.originID = originID
        self.name = name
        self.photo = photo
        self.fragrance = fragrance
        self.flavor = flavor
        self.aftertaste = aftertaste
        self.acidity = acidity
        self.body = body
        self.balance = balance
        self.uniformity = uniformity
        self.cleanCups = cleanCups
        self.sweetness = sweetness
        self.overall = overall
        self.description = description
        self.cupping = cupping
        self.advantage = advantage
        self.disadvantage = disadvantage
        self.location = location
