from app.models.user import User
from app.models.order_line import OrderLine

class Order:
    def __init__(self, user, cart):
        self.user_name = user.name
        self.user_email = user.email
        self.total_price = cart.total_price()
        self.lines = [
            OrderLine(prod.name, prod.price, qty) for prod, qty in cart.items.items()
        ]

    @classmethod
    def from_repository(cls, order_db):
        from app.models.cart import Cart

        user = User(
            order_db.user_name,
            order_db.user_email)

        order = cls(user, Cart())

        order.user_name = order_db.user_name
        order.user_email = order_db.user_email
        order.total_price = order_db.total_price
        order.lines = [
                OrderLine(
                    product_name=line.product.name,
                    product_price=line.price,
                    quantity=line.quantity
                ) for line in order_db.order_lines
            ]

        return order
