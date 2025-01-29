from app.db import db, UserDB


class User:
    def __init__(self, user_id = None, name = None, email = None, password = None):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password

    def save_to_db(self):
        if UserDB.query.filter_by(email=self.email).first():
            raise ValueError("Email already exists.")
        user_db = UserDB(name=self.name, email=self.email, password=self.password)
        db.session.add(user_db)
        db.session.commit()
        return user_db.id

    def fetch_from_db(self, user_id):
        user = db.session.query(UserDB).filter_by(id=user_id).first()

        if not user:
            raise ValueError("User not found.")

        self.id = user_id
        self.name = user.name
        self.email = user.email
        self.password = user.password