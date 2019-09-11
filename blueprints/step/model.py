from blueprints import db
from flask_restful import fields

class Steps(db.Model):
    __tablename__ = "steps"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipeID = db.Column(db.Integer, nullable=False, default=0)
    stepNumber = db.Column(db.Integer, nullable=False, default=0)
    stepTypeID = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    responseFields = {
        'id': fields.Integer,
        'recipeID' : fields.Integer,
        'stepNumber' : fields.Integer,
        'stepTypeID': fields.Integer,
        'note' : fields.String,
        'time' : fields.Integer,
        'amount' : fields.Integer
    }

    def __init__(self, recipeID, stepNumber, stepTypeID, note, time, amount):
        self.recipeID = recipeID
        self.stepNumber = stepNumber
        self.stepTypeID = stepTypeID
        self.note = note
        self.time = time
        self.amount = amount

    
