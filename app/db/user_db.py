from app.db import db


class UserDB(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    orders = db.relationship('OrderDB', back_populates='user')
    cart = db.relationship('CartDB', back_populates='user', uselist=False)

