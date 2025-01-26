from run.models.OrderLine import OrderLine


class Order:
    MAX_ORDER_VALUE = 30000

    def __init__(self, customer, cart):
        self.customer = customer
        self.cart = cart

        self.order_lines = [
            OrderLine(item, item.price) for item in cart.items
        ]

    def __str__(self):
        order_summary = "\n".join(str(line) for line in self.order_lines)
        return f"Order for {self.customer.name}:\n{order_summary}\nTotal: {self.total()} PLN\n"

    def total(self):
        return sum(line.price_at_order_time for line in self.order_lines)

    def place_order(self):
        if self.cart.total() > self.MAX_ORDER_VALUE:
            print("Order cannot be placed. Total value exceeds 30,000 PLN.")
        else:
            print(f"Order placed successfully for {self.customer.name}.\n")
            print(self)
