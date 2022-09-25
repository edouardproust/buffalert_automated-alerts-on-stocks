from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import session
from models import db, update, delete


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(255))
    alerts = db.relationship('Alert', backref='user', lazy=True)
 

def find(id=None):
    """Get the User from his/her id. If no id provided, returns the connected user.

    id : int
        The user id. Default: session["user_id"] (connected user id)
    """
    if not id and session:
        id = session["user_id"]
    return User.query.get(id)


def find_by_email(email):
    return User.query.filter_by(email=email).first()


def create(email, password):
    hash = generate_password_hash(password)
    user = User(email=email, hash=hash) 
    db.session.add(user)
    db.session.commit()
    return user
