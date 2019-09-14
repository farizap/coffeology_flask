from blueprints import db
from flask_restful import fields

class Reviews(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    recipeID = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    photo = db.Column(db.String(250), nullable=False)

responseFields =  {
    'id' : flieds.Integer,
    'userID' : flieds.Integer,
    'recipeID' : flieds.Integer,
    'content' : fields.Text,
    'rating' : fields.Integer,
    'createdAt' : fields.DateTime,
    'photo' :  fields.String,
}

def __init__(self, userID, recipeID, content, rating, createdAt, photo):
        self.userID = userID
        self.recipeID = recipeID
        self.content = content
        self.rating = rating
        self.createdAt = createdAt
        self.photo = photo
