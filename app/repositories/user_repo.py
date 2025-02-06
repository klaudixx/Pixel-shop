from sqlalchemy.exc import IntegrityError

from app.db import db, UserDB


class UserRepository:
    @staticmethod
    def save_in_db(user, user_db=None):
        if user_db:
            user_db.name = user.name
            user_db.email = user.email
        else:
            user_db = UserDB(name=user.name, email=user.email)
            db.session.add(user_db)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise EmailAlreadyExistsError("User with this email already exists")

        return user_db.id

    @staticmethod
    def fetch_by_id(user_id):
        user_db = db.session.query(UserDB).filter_by(id=user_id).first()

        if not user_db:
            raise UserNotFoundError("User not found")

        return user_db


class EmailAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass
