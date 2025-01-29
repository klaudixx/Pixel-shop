from flask import Blueprint, request, jsonify

from app.models import User


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = User(name=data['name'], email=data['email'], password=data['password'])
        user_id = user.save_to_db()
        return jsonify({'message': 'User created successfully.','id':user_id}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_by_id(user_id):
    user = User()
    try:
        user.fetch_from_db(user_id)
        return jsonify(vars(user)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
