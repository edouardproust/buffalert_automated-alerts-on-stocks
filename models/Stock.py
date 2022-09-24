from datetime import datetime

if __name__ == "models.Stock": # cli
    from models import db
else: # flask run
    from ..models import db, update, delete


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('stock_category.id'), nullable=False)
    ticker = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def find(id):
    """Retrieve an alert from its ID"""
    return Stock.query.get(id)


def get_by_ticker(ticker):
    return Stock.query.filter_by(ticker=ticker).first()


def update(ticker, price, name=None, category_id=None):
    # Check if the stock is in db
    stock = Stock.query.filter_by(ticker=ticker).first()
    
    if not stock:
        # Create entity
        stock = Stock()
        stock.category_id = category_id
        stock.ticker = ticker
        stock.name = name
    # Save entity
    stock.price = price
    stock.updated_at = datetime.now()
    db.session.add(stock)
    db.session.commit()
    # Return
    return stock