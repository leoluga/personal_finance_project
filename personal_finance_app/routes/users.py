from flask import Blueprint, render_template, request, redirect, url_for
from models import User, db

users_bp = Blueprint('users', __name__)

# View all users
@users_bp.route('/')
def view_users():
    users = db.session.query(User).all()
    return render_template('users/view_users.html', users=users)

# Add a new user
@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.view_users'))
    return render_template('users/add_user.html')

# Edit an existing user
@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.session.query(User).filter_by(user_id=user_id).one()
    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect(url_for('users.view_users'))
    return render_template('users/edit_user.html', user=user)

# Delete a user
@users_bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = db.session.query(User).filter_by(user_id=user_id).one()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.view_users'))
