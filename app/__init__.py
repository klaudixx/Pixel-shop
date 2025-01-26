import os.path

from flask import Flask
from app.db import db
from app.routes import *


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.json.sort_keys = False

    db.init_app(app)

    if not os.path.exists("shop.db"):
        with app.app_context():
            db.create_all()

    from app.routes.user import user_bp
    app.register_blueprint(user_bp)

    return app
