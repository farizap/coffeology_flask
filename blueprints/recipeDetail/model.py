from blueprints import db
from flask_restful import fields


class RecipeDetails(db.Model):
    __tablename__ = "recipeDetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipeID = db.Column(db.Integer, nullable=False)
    fragrance = db.Column(db.Float, nullable=False)
    aroma = db.Column(db.Float, nullable=False)
    cleanliness = db.Column(db.Float, nullable=False)
    sweetness = db.Column(db.Float, nullable=False)
    taste = db.Column(db.Float, nullable=False)
    acidity = db.Column(db.Float, nullable=False)
    aftertaste = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    globalTaste = db.Column(db.Float, nullable=False)
    body = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(250), nullable=False)
    grindSize = db.Column(db.Integer, nullable=False)
    waterTemp = db.Column(db.Integer, nullable=False)

    responseFields = {
        'id': fields.Integer,
        'recipeID': fields.Integer,
        'fragrance': fields.Float,
        'aroma': fields.Float,
        'cleanliness': fields.Float,
        'sweetness': fields.Float,
        'taste': fields.Float,
        'acidity': fields.Float,
        'aftertaste': fields.Float,
        'balance': fields.Float,
        'globalTaste': fields.Float,
        'body': fields.Float,
        'note': fields.String,
        'grindSize': fields.Integer,
        'waterTemp': fields.Integer,
    }

    def __init__(self, recipeID, fragrance, aroma, cleanliness, sweetness,
                 taste, acidity, aftertaste, balance, globalTaste, body, note,
                 grindSize, waterTemp):
        self.recipeID = recipeID
        self.fragrance = fragrance
        self.aroma = aroma
        self.cleanliness = cleanliness
        self.sweetness = sweetness
        self.taste = taste
        self.acidity = acidity
        self.aftertaste = aftertaste
        self.balance = balance
        self.globalTaste = globalTaste
        self.body = body
        self.note = note
        self.grindSize = grindSize
        self.waterTemp = waterTemp
