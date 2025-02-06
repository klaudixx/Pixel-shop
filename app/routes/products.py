from flask import Blueprint, request, jsonify

from app.models.product import Product, NoDataProvidedError
from app.repositories.product_repo import ProductRepository, ProductNotFoundError

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    try:
        product = Product(name, price)
        product_id = ProductRepository.save_in_db(product)

        return jsonify({'message': 'Product created successfully.', 'product_id': product_id}), 201
    except NoDataProvidedError as e:
        return jsonify({'message': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_by_id(product_id):
    try:
        product_db = ProductRepository.fetch_by_id(product_id)
        product = Product.from_repository(product_db)

        return jsonify(vars(product)), 200
    except ProductNotFoundError as e:
        return jsonify({'message': str(e)}), 404

@products_bp.route('/', methods=['GET'])
def get_all():
    return jsonify({'products': [product.to_dict() for product in ProductRepository.fetch_all()]}), 200

@products_bp.route('/<int:product_id>', methods=['PATCH'])
def update_price(product_id):
    price = request.get_json().get('price')

    try:
        product_db = ProductRepository.fetch_by_id(product_id)
        product = Product.from_repository(product_db)
        product.update_price(price)
        ProductRepository.save_in_db(product, product_db)

        return jsonify({'message': 'Product price updated successfully.', 'data': vars(product)}), 200
    except ProductNotFoundError as e:
        return jsonify({'message': str(e)}), 404
    except NoDataProvidedError as e:
        return jsonify({'message': str(e)}), 400
