from flask import Blueprint, jsonify
from app.db.order import OrderDB

order_bp = Blueprint('orders', __name__, url_prefix='/order')

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderDB.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order_data = {
        'id': order.id,
        'total_price': order.total_price,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'order_lines': []
    }

    for line in order.order_lines:
        order_data['order_lines'].append({
            'product_id': line.product_id,
            'product_name': line.product.name,
            'price': line.price,
            'quantity': line.quantity
        })

    return jsonify(order_data), 200
