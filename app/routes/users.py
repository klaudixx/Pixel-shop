from flask import Blueprint, request, jsonify
from app.models.user import User, NoDataProvidedError
from app.repositories.user_repo import UserRepository, EmailAlreadyExistsError, UserNotFoundError

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    try:
        user = User(name, email)
        user_id = UserRepository.save_in_db(user=user)

        return jsonify({"message": "User created successfully.", "user_id": user_id}), 201
    except NoDataProvidedError as e:
        return jsonify({"message": str(e)}), 400
    except EmailAlreadyExistsError as e:
        return jsonify({"message": str(e)}), 409

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_by_id(user_id):
    try:
        user_db = UserRepository.fetch_by_id(user_id)
        user = User.from_repository(user_db)

        return jsonify(vars(user)), 200
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@users_bp.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    try:
        user_db = UserRepository.fetch_by_id(user_id)
        user = User.from_repository(user_db)
        user.update(name, email)
        UserRepository.save_in_db(user, user_db)

        return jsonify({"message": "User updated successfully.", "data": vars(user)}), 200
    except UserNotFoundError as e:
        return jsonify({"message": str(e)}), 404
    except NoDataProvidedError as e:
        return jsonify({"message": str(e)}), 400
    except EmailAlreadyExistsError as e:
        return jsonify({"message": str(e)}), 409
