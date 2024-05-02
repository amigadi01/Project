from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    data = db.Column(db.DateTime(timmezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Coumn(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Coumn(db.String(150))
    notes = db.reltaionship('Note')
