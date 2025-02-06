from app.db import db

class OrderDB(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Powiązanie z użytkownikiem

    user = db.relationship('UserDB', back_populates='orders')

    order_lines = db.relationship('OrderLineDB', back_populates='order', cascade='all, delete-orphan')
