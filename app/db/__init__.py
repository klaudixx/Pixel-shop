from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .order import OrderDB
from .order_line import OrderLineDB
from .product import ProductDB
from .user import UserDB

