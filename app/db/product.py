from app.db import db

class ProductDB(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    order_lines = db.relationship('OrderLineDB', back_populates='product')
