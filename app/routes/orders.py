from flask import Blueprint, session, jsonify
from app.db import db, OrderDB, OrderLineDB


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/checkout', methods=['POST'])
def create_order():
    cart = session.get('cart', [])

    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    total_price = sum(item['price'] * item['quantity'] for item in cart)

    if total_price > 30000:
        return jsonify({'error': 'Order exceeds the maximum allowed value (30,000)'}), 400

    order = OrderDB(total_price=total_price)
    db.session.add(order)
    db.session.commit()

    for item in cart:
        order_line = OrderLineDB(
            order_id=order.id,
            product_id=item['product_id'],
            price=item['price'],
            quantity=item['quantity']
        )
        db.session.add(order_line)

    db.session.commit()

    session['cart'] = []
    session.modified = True

    return jsonify({'message': 'Order created successfully', 'order_id': order.id}), 201