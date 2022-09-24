from flask_sqlalchemy import SQLAlchemy

if __name__ == "models": # cli
    import config as c
else: # flask run
    from .. import config as c


db = SQLAlchemy(c.get_app())


# Common methods for all models

def update(entity, data):
    for i in data:
        setattr(entity,i, data[i])
    db.session.commit()

def delete(entity):
    db.session.delete(entity)
    db.session.commit()


# Import models

from . import Stock, Alert, StockCategory, User