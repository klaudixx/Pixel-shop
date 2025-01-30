from flask import Blueprint, session, jsonify

from app.db import UserDB
from app.models import Cart, Order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/create', methods=['POST'])
def create_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User is not logged in.'}), 400

    user = UserDB.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    cart = Cart(session.get('cart'))
    order = Order(cart=cart, user=user)

    try:
        order.save_to_db()
        cart.clear()
        session['cart'] = cart.items
        session.modified = True
        return jsonify({'message': 'Order created successfully.', 'order_id': order.order_id}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    try:
        order = Order.fetch_from_db(order_id)
        return jsonify(vars(order)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
