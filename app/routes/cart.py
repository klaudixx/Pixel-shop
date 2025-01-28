from flask import Blueprint, request, jsonify, session
from app.db import db, ProductDB


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = db.session.get(ProductDB, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    cart = session['cart']
    cart.append({
        'product_id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': quantity
    })
    session.modified = True

    return jsonify({'message': 'Product added to cart', 'cart': cart}), 200

@cart_bp.route('/', methods=['GET'])
def view_cart():
    return jsonify(session['cart']), 200
