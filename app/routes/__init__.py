from flask import Blueprint

from .users import users_bp
from .products import products_bp
from .cart import cart_bp
from .orders import orders_bp


api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(products_bp)
api_bp.register_blueprint(cart_bp)
api_bp.register_blueprint(orders_bp)
