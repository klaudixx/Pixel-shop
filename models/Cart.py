
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product):
        self.items.append(product)
        print(f"Product '{product.name}' added to cart.\n")

    def total(self):
        return sum(item.price for item in self.items)

    def __str__(self):
        return f"Cart total: {self.total()} PLN"