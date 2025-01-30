from sqlalchemy.orm import joinedload
from app.db import db, OrderDB, OrderLineDB
from app.models.user import User

class Order:
    def __init__(self, user=None, order_id=None, cart=None, total_price=None, order_lines=None, created_at=None):
        self.user = user

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
        if not self.user or not self.user.id:
            raise ValueError("Order must be associated with a user.")

        order = OrderDB(total_price=self.total_price, user_id=self.user.id)
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

    @classmethod
    def fetch_from_db(cls, order_id):
        order = db.session.query(OrderDB).filter_by(id=order_id) \
            .options(joinedload(OrderDB.user), joinedload(OrderDB.order_lines).joinedload(OrderLineDB.product)) \
            .first()

        if not order:
            raise ValueError("Order not found.")

        user = User.fetch_from_db(user_id=order.user_id)
        user_dict = {'id': user.id, 'name': user.name, 'email': user.email}

        order_lines = [{
            'product_name': ol.product.name,
            'price': ol.price,
            'quantity': ol.quantity,
        } for ol in order.order_lines]

        return cls(user=user_dict, order_id=order.id, total_price=order.total_price, created_at=order.created_at, order_lines=order_lines)
