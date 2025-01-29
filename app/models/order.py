from sqlalchemy.orm import joinedload

from app.db import db, OrderDB, OrderLineDB, ProductDB


class Order:
    def __init__(self, order_id = None, cart = None, total_price = None, order_lines = None, created_at = None):
        if cart:
            self.cart = cart.get()
            self.total_price = self.cart['total']
        else:
            self.order_id = order_id
            self.total_price = total_price
            self.created_at = created_at
            self.order_lines = order_lines

    def save_to_db(self):
        if not self.cart['products']:
            raise ValueError("Cart is empty.")

        if self.cart['total'] > 30000:
            raise ValueError("Order exceeds the maximum allowed value (30,000).")

        order = OrderDB(total_price=self.total_price)
        db.session.add(order)
        db.session.commit()

        for item in self.cart['products']:
            order_line = OrderLineDB(
                order_id=order.id,
                product_id=item['product_id'],
                price=item['price'],
                quantity=item['quantity']
            )
            db.session.add(order_line)
        db.session.commit()

        self.order_id = order.id


    def fetch_from_db(self, order_id):
        order = db.session.query(OrderDB).filter_by(id=order_id). \
            options(joinedload(OrderDB.order_lines).joinedload(OrderLineDB.product)).first()

        if not order:
            raise ValueError("Order not found.")

        self.order_id = order.id
        self.total_price = order.total_price
        self.created_at = order.created_at

        self.order_lines = []
        for order_line in order.order_lines:
            self.order_lines.append({
                'product_name': order_line.product.name,
                'price': order_line.price,
                'quantity': order_line.quantity,
            })


