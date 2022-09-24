if __name__ == "models.StockCategory": # cli
    from models import db
else: # flask run
    from ..models import db, update, delete


class StockCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    description = db.Column(db.Text)
    stocks = db.relationship('Stock', backref='stock_category', lazy=True)


def get_by_name(name):
    # Ensure that the category exists
    category = StockCategory.query.filter_by(name=name).first()
    if not category:
        category = create(name)
    return category


def create(name):
    category = StockCategory()
    category.name = name 
    db.session.add(category)
    db.session.commit()
    return category