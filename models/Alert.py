from calendar import week
from flask import session
from .Stock import Stock
from models import db, update, delete
from helpers._string import tupleToString

class Alert(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String(1), nullable=False)
    day = db.Column(db.Integer)
    weekday = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    stock = db.relationship('Stock', backref='user', uselist=False)


def all():
    """Get a list of all alerts"""
    return Alert.query.all()


def find(id):
    """Retrieve an alert from its ID"""
    return Alert.query.get(id)


def find_by_user(user_id=None):
    """Get a list of alerts for a given user (ordered by ticker, then by alert price)"""

    if not user_id:
        user_id = session['user_id']
    return (Alert.query
        .filter_by(user_id=user_id)
        .join(Stock)
        .order_by(Stock.ticker, Alert.price)
        .all()
    )


def create(stock_id, price, frequency, hour, weekday, day):
    # Create entity
    alert = Alert()
    alert.user_id = session['user_id']
    alert.stock_id = stock_id
    alert.price = price
    alert.frequency = frequency
    alert.hour = hour,
    alert.weekday = weekday,
    alert.day = day
    # Fix tuple bug in commit
    alert.hour = tupleToString(alert.hour)
    alert.weekday = tupleToString(alert.weekday)
    # Save it
    db.session.add(alert)
    db.session.commit()
    # Return
    return alert
