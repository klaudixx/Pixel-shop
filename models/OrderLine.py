class OrderLine:
    def __init__(self, product, price_at_order_time):
        self.product = product
        self.price_at_order_time = price_at_order_time

    def __str__(self):
        return f"{self.product.name}: {self.price_at_order_time} PLN"
