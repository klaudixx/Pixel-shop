from app.db import ProductDB, db


class ProductRepository:
    @staticmethod
    def save_in_db(product, product_db=None):
        if product_db:
            product_db.price = product.price
        else:
            product_db = ProductDB(name=product.name, price=product.price)
            db.session.add(product_db)

        db.session.commit()

        return product_db.id

    @staticmethod
    def fetch_by_id(product_id):
        product_db = db.session.query(ProductDB).filter_by(id=product_id).first()

        if not product_db:
            raise ProductNotFoundError("Product not found")

        return product_db

    @staticmethod
    def fetch_all():
        return db.session.query(ProductDB).all()


class ProductNotFoundError(Exception):
    pass
