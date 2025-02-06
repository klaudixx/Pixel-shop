from app.db import OrderDB, db, OrderLineDB


class OrderRepository:
    @staticmethod
    def save_in_db(order, user_id, cart_items):
        order_db = OrderDB(
            user_id=user_id,
            user_name=order.user_name,
            user_email=order.user_email,
            total_price=order.total_price
        )
        db.session.add(order_db)
        db.session.flush()

        for cart_item in cart_items:
            order_line = OrderLineDB(
                order_id=order_db.id,
                product_id=cart_item.product_id,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            db.session.add(order_line)
            db.session.commit()

        return order_db.id

    @staticmethod
    def fetch_by_id(order_id):
        order_db = db.session.query(OrderDB).filter_by(id=order_id).first()

        if not order_db:
            raise OrderNotFoundError("Order not found")

        return order_db


class OrderNotFoundError(Exception):
    pass