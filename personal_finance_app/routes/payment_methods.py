from flask import Blueprint, render_template, request, redirect, url_for
from models import PaymentMethod, User, db

payment_methods_bp = Blueprint('payment_methods', __name__)

# View all payment methods
@payment_methods_bp.route('/')
def view_payment_methods():
    payment_methods = db.session.query(PaymentMethod).all()
    return render_template('payment_methods/view_payment_methods.html', payment_methods=payment_methods)

# Add a new payment method
@payment_methods_bp.route('/add', methods=['GET', 'POST'])
def add_payment_method():
    users = db.session.query(User).all()  # Fetch users for dropdown
    if request.method == 'POST':
        method_name = request.form['method_name']
        user_id = request.form['user_id']
        bank_name = request.form['bank_name']
        new_payment_method = PaymentMethod(method_name=method_name, user_id=user_id, bank_name=bank_name)
        db.session.add(new_payment_method)
        db.session.commit()
        return redirect(url_for('payment_methods.view_payment_methods'))
    return render_template('payment_methods/add_payment_method.html', users=users)

# Edit an existing payment method
@payment_methods_bp.route('/edit/<int:payment_method_id>', methods=['GET', 'POST'])
def edit_payment_method(payment_method_id):
    payment_method = db.session.query(PaymentMethod).filter_by(payment_method_id=payment_method_id).one()
    users = db.session.query(User).all()  # Fetch users for dropdown
    if request.method == 'POST':
        payment_method.method_name = request.form['method_name']
        payment_method.user_id = request.form['user_id']
        payment_method.bank_name = request.form['bank_name']
        db.session.commit()
        return redirect(url_for('payment_methods.view_payment_methods'))
    return render_template('payment_methods/edit_payment_method.html', payment_method=payment_method, users=users)

# Delete a payment method
@payment_methods_bp.route('/delete/<int:payment_method_id>', methods=['GET', 'POST'])
def delete_payment_method(payment_method_id):
    payment_method = db.session.query(PaymentMethod).filter_by(payment_method_id=payment_method_id).one()
    db.session.delete(payment_method)
    db.session.commit()
    return redirect(url_for('payment_methods.view_payment_methods'))
