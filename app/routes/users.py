from flask import Blueprint, request, jsonify
from app.db import db, UserDB


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if UserDB.query.filter_by(email=email).first():
        return jsonify({'error': 'Email is already in use'}), 400

    user = UserDB(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Customer registered successfully', 'id': user.id}), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(UserDB, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200
