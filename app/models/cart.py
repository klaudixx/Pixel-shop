from app.models import Product
from app.models.order import Order


class Cart:
    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity=1):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def clear(self):
        self.items = {}

    def total_price(self):
        return sum(product.price * quantity for product, quantity in self.items.items())

    def checkout(self, user):
        if self.total_price() > 30000:
            raise ValueExceedsLimitError("Order value exceeds 30,000!")
        return Order(user, self)

    @classmethod
    def from_repository(cls, cart_db):
        if not cart_db:
            return cls()

        cart = cls()

        for item in cart_db.cart_items:
            product = Product.from_repository(item.product)
            cart.add_product(product, item.quantity)

        return cart

class ValueExceedsLimitError(Exception):
    pass
