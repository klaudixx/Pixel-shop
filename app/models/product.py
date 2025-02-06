class Product:
    def __init__(self, name, price):
        if not name or not price:
            raise NoDataProvidedError("Name and price are required.")

        self.name = name
        self.price = price

    def update_price(self, price):
        if not price:
            raise NoDataProvidedError("Price is required.")

        self.price = price

    @classmethod
    def from_repository(cls, product_db):
        return cls(product_db.name, product_db.price)


class NoDataProvidedError(Exception):
    pass