from flask import Blueprint, request, jsonify

from app.models import Product, User
from app.models.cart import Cart, ValueExceedsLimitError
from app.repositories.cart_repo import CartRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository, ProductNotFoundError
from app.repositories.user_repo import UserRepository, UserNotFoundError

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/<int:user_id>', methods=['POST'])
def add_product_to_cart(user_id):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    try:
        user_db = UserRepository.fetch_by_id(user_id)
        product_db = ProductRepository.fetch_by_id(product_id)
        cart_db = CartRepository.fetch_by_user_id(user_id)

        product = Product.from_repository(product_db)
        cart = Cart.from_repository(cart_db)
        cart.add_product(product, quantity)

        CartRepository.add_product_and_save(user_id, product_id, quantity)
        return jsonify({'message': 'Product added to cart successfully.'}), 201
    except UserNotFoundError as e:
        return jsonify({'message': str(e)}), 404
    except ProductNotFoundError as e:
        return jsonify({'message': str(e)}), 404


@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_db = CartRepository.fetch_by_user_id(user_id)
    cart = Cart.from_repository(cart_db)

    cart_response = [
        {
            "name": product.name,
            "price": product.price,
            "quantity": quantity
        }
        for product, quantity in cart.items.items()
    ]

    return jsonify(cart_response), 201

@cart_bp.route('/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    try:
        user_db = UserRepository.fetch_by_id(user_id)
        cart_db = CartRepository.fetch_by_user_id(user_id)

        cart = Cart.from_repository(cart_db)
        cart.clear()

        CartRepository.clear_cart(user_id)
        return jsonify({'message': 'Cart cleared successfully.'}), 200
    except UserNotFoundError as e:
        return jsonify({'message': str(e)}), 404

@cart_bp.route('/<int:user_id>/checkout', methods=['POST'])
def checkout_cart(user_id):
    try:
        user_db = UserRepository.fetch_by_id(user_id)
        cart_db = CartRepository.fetch_by_user_id(user_id)
        cart = Cart.from_repository(cart_db)

        user = User.from_repository(user_db)
        order = cart.checkout(user)

        order_id = OrderRepository.save_in_db(order, user_db.id, cart_db.cart_items)
        return jsonify({'message': 'Order placed successfully.', 'order_id': order_id}), 201
    except UserNotFoundError as e:
        return jsonify({'message': str(e)}), 404
    except ValueExceedsLimitError as e:
        return jsonify({'message': str(e)}), 400
