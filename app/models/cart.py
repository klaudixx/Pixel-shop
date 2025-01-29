from app import db
from app.db import ProductDB


class Cart:
    def __init__(self, session_cart):
        self.items = session_cart or []

    def add_product(self, product, quantity):
        for item in self.items:
            if item['product_id'] == product.id:
                item['quantity'] += quantity
                return
        self.items.append({
            'product_id': product.id,
            'quantity': quantity
        })

    def clear(self):
        self.items.clear()

    def get(self):
        total = 0
        products = []

        for item in self.items:
            product = db.session.query(ProductDB).filter_by(id=item['product_id']).first()

            if product:
                item_total = product.price * item['quantity']
                total += item_total

                products.append({
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': item['quantity'],
                    'total': item_total
                })

        return {
            'total': total,
            'products': products
        }
