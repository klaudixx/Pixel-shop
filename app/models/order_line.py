class OrderLine:
    def __init__(self, product_name, product_price, quantity):
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity

    def __repr__(self):
        return f"OrderLine(product_name={self.product_name}, price={self.product_price}, quantity={self.quantity})"