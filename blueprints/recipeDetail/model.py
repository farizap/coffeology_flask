from blueprints import db
from flask_restful import fields


class RecipeDetails(db.Model):
    __tablename__ = "recipeDetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipeID = db.Column(db.Integer, nullable=False)
    fragrance = db.Column(db.Integer, nullable=False)
    aroma = db.Column(db.Integer, nullable=False)
    cleanliness = db.Column(db.Integer, nullable=False)
    sweetness = db.Column(db.Integer, nullable=False)
    taste = db.Column(db.Integer, nullable=False)
    acidity = db.Column(db.Integer, nullable=False)
    aftertaste = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    globalTaste = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(250), nullable=False)

    responseFields = {
        'id': fields.Integer,
        'recipeID': fields.Integer,
        'fragrance': fields.Integer,
        'aroma': fields.Integer,
        'cleanliness': fields.Integer,
        'sweetness': fields.Integer,
        'taste': fields.Integer,
        'acidity': fields.Integer,
        'aftertaste': fields.Integer,
        'balance': fields.Integer,
        'globalTaste': fields.Integer,
        'note': fields.String
    }

    def __init__(self, recipeID, fragrance, aroma, cleanliness, sweetness,
                 taste, acidity, aftertaste, balance, globalTaste, note):
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
        self.note = note
