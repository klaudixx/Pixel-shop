from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import *

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super_secret_key'

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.products import products_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(products_bp)

    return app
