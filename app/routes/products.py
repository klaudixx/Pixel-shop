from flask import Blueprint, request, jsonify
from app.db import db, ProductDB


products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()

    product = ProductDB(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product registered successfully', 'id': product.id, 'name': product.name, 'price': product.price}), 201

@products_bp.route('/', methods=['GET'])
def get_products():
    products = ProductDB.query.all()
    result = [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]
    return jsonify(result), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.session.get(ProductDB, product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 200

@products_bp.route('/<int:product_id>', methods=['PUT'])
def change_price(product_id):
    data = request.get_json()
    product = ProductDB.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product price updated successfully'}), 200





