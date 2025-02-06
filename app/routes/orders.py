from flask import Blueprint, session, jsonify

from app.db import UserDB
from app.models import Cart, Order
from app.repositories.order_repo import OrderRepository, OrderNotFoundError

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    try:
        order_db = OrderRepository.fetch_by_id(order_id)
        order = Order.from_repository(order_db)
        order_response = {
            "user_name": order.user_name,
            "user_email": order.user_email,
            "total_price": order.total_price,
            "lines": [
                {
                    "product_name": line.product_name,
                    "price": line.product_price,
                    "quantity": line.quantity
                }
                for line in order.lines
            ]
        }

        return jsonify(order_response), 200
    except OrderNotFoundError as e:
        return jsonify({'message': str(e)}), 404
