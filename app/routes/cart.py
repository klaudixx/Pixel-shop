from flask import Blueprint, request, jsonify, session

from app.models import Cart, Product


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    try:
        product = Product.fetch_from_db(data['product_id'])
        cart = Cart(session.get('cart'))
        cart.add_product(product, data['quantity'])
        session['cart'] = cart.items
        session.modified = True
        return jsonify({'message': 'Product added to cart.', 'cart': cart.get()}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    cart = Cart(session.get('cart'))
    cart.clear()
    session['cart'] = cart.items
    session.modified = True
    return jsonify({'message': 'Cart cleared.', 'cart': cart.items}), 200