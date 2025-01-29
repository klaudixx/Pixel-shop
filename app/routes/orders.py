from flask import Blueprint, session, jsonify

from app.models import Cart, Order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/create', methods=['POST'])
def create_order():
    cart = Cart(session.get('cart'))
    order = Order(cart=cart)

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
    order = Order()

    try:
        order.fetch_from_db(order_id)
        return jsonify(vars(order)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
