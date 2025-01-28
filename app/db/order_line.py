from app.db import db

class OrderLineDB(db.Model):
    __tablename__ = 'order_lines'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('OrderDB', back_populates='order_lines')
    product = db.relationship('ProductDB', back_populates='order_lines')
