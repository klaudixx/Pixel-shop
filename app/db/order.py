from app.db import db

class OrderDB(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order_lines = db.relationship('OrderLineDB', back_populates='order', cascade='all, delete-orphan')
