from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.db import UserDB

class User:
    def __init__(self, user_id=None, name=None, email=None, password=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def fetch_from_db(cls, user_id=None, user_email=None):
        if user_id:
            user = db.session.query(UserDB).filter_by(id=user_id).first()
        elif user_email:
            user = db.session.query(UserDB).filter_by(email=user_email).first()

        if not user:
            raise ValueError("User not found.")

        return cls(user_id=user.id, name=user.name, email=user.email, password=user.password)

    def save_to_db(self):
        if UserDB.query.filter_by(email=self.email).first():
            raise ValueError("Email already exists.")
        self.password = generate_password_hash(self.password)
        user_db = UserDB(name=self.name, email=self.email, password=self.password)
        db.session.add(user_db)
        db.session.commit()
        self.id = user_db.id

    def update(self):
        if self.id is None:
            raise ValueError("Cannot update a user without an ID.")

        user = db.session.query(UserDB).filter_by(id=self.id).first()

        if not user:
            raise ValueError("User not found.")

        user.name = self.name
        user.email = self.email
        if self.password:
            user.password = generate_password_hash(self.password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def login(self, password):
        if self.check_password(password):
            return {'message': 'Login successful', 'user_id': self.id}
        else:
            raise ValueError("Invalid credentials.")
