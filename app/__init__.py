import os.path
from flask import Flask, session

from app.db import db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.json.sort_keys = False

    db.init_app(app)

    @app.before_request
    def init_cart():
        if 'cart' not in session:
            session['cart'] = []

    if not os.path.exists("shop.db"):
        with app.app_context():
            db.create_all()

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
