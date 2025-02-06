from app.models.order_line import OrderLine

class Order:
    def __init__(self, user, cart):
        self.user_name = user.name
        self.user_email = user.email
        self.total_price = cart.total_price()
        self.lines = [
            OrderLine(prod.name, prod.price, qty) for prod, qty in cart.items.items()
        ]
