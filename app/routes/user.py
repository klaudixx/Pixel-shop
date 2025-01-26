from flask import Blueprint, render_template, request, redirect, url_for
from app.db import db
from app.db.customer import CustomerDB

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if CustomerDB.query.filter_by(email=email).first():
            return "Email already exists"

        new_user = CustomerDB(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user.create_user'))

    return render_template('create_user.html')

@user_bp.route('/')
def list_users():
    users = CustomerDB.query.all()
    return render_template('list_users.html', users=users)
