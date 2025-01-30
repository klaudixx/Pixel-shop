from flask import Blueprint, request, jsonify, session

from app.models import User


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = User(name=data['name'], email=data['email'], password=data['password'])
        user.save_to_db()
        return jsonify({'message': 'User created successfully.','data': vars(user)}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_by_id(user_id):
    try:
        user = User.fetch_from_db(user_id = user_id)
        return jsonify(vars(user)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404

@users_bp.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        user = User.fetch_from_db(user_id)
        data = request.get_json()

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']

        user.update()
        return jsonify(vars(user)), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 404

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        user = User.fetch_from_db(user_email=data['email'])
        response = user.login(data['password'])
        session['user_id'] = user.id
        return jsonify(response), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 400