from app.db import db, ProductDB


class Product:
    def __init__(self, product_id=None, name=None, price=None):
        self.id = product_id
        self.name = name
        self.price = price

    @classmethod
    def fetch_from_db(cls, product_id):
        product = db.session.query(ProductDB).filter_by(id=product_id).first()
        if not product:
            raise ValueError("Product not found.")
        return cls(product_id=product.id, name=product.name, price=product.price)

    def save_to_db(self):
        product_db = ProductDB(name=self.name, price=self.price)
        db.session.add(product_db)
        db.session.commit()
        self.id = product_db.id

    def update_price(self, new_price):
        self.price = new_price
        product = db.session.query(ProductDB).filter_by(id=self.id).first()
        product.price = new_price
        db.session.commit()
