from flask import Blueprint, request, jsonify

from app.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/add', methods=['POST'])
def create_product():
    data = request.get_json()

    product = Product(name=data['name'], price=data['price'])
    product.save_to_db()

    return jsonify({'message': 'Product added successfully.','data': vars(product)}), 201

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_by_id(product_id):
    product = Product()

    try:
        product.fetch_from_db(product_id)
        return jsonify(vars(product)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

@products_bp.route('/<int:product_id>/price', methods=['PATCH'])
def update_price(product_id):
    data = request.get_json()
    product = Product()
    try:
        product.fetch_from_db(product_id)
        product.update_price(data['price'])
        return jsonify({'message': 'Product price updated successfully.', 'data': vars(product)}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404