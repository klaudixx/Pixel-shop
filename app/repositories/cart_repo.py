from app.db import CartDB, db, ProductDB
from app.db.cart_item_db import CartItemDB


class CartRepository:
    @staticmethod
    def fetch_by_user_id(user_id):
        cart_db = CartDB.query.filter_by(user_id=user_id).first()

        return cart_db

    @staticmethod
    def add_product_and_save(user_id, product_id, quantity):

        if not quantity:
            quantity = 1

        cart = CartRepository.fetch_by_user_id(user_id)

        if not cart:
            cart = CartDB(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        cart_item = db.session.query(CartItemDB).filter_by(cart_id=cart.id, product_id=product_id).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItemDB(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()

    @staticmethod
    def clear_cart(user_id):
        cart = CartRepository.fetch_by_user_id(user_id)
        db.session.delete(cart)
        db.session.commit()
