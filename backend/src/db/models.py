from flask_sqlalchemy import SQLAlchemy
from app import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Book %r>' & self.id


def dropEverything():
    db.drop_all()

def createEverything():
    db.drop_all()