class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price} PLN\n"

    def change_price(self, new_price):
        old_price = self.price
        self.price = new_price
        print(f"Price changed {old_price} -> {new_price}\n")