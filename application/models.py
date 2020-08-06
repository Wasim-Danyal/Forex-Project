from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    base_currency = db.Column(db.String(5), nullable=False) 
    new_currency = db.Column(db.String(5), nullable=False) 
    bid_rate = db.Column(db.Integer(10), nullable=False)
    ask_rate = db.Column(db.Integer(10), nullable=False)
=======
    base_currency = db.column(db.String(5), nullable=False) 
    new_currency = db.column(db.String(5), nullable=False) 
    bid_rate = db.column(db.Integer(10), nullable=False)
    ask_rate = db.column(db.Integer(10), nullable=False)
>>>>>>> development


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
