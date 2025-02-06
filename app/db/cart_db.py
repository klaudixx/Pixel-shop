from app.db import db


class CartDB(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('UserDB', back_populates='cart')
    cart_items = db.relationship('CartItemDB', back_populates='cart', cascade="all, delete-orphan")