from flask import Blueprint, render_template
from app.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def product_list():
    products = Product.query.all()
    return render_template('products.html', products=products)
