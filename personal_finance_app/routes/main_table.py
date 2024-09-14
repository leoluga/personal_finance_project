from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import User, Category, SubCategory, MainTable, PaymentMethod, db

main_table_bp = Blueprint('main_table', __name__)

@main_table_bp.route('/')
def view_main_table():
    records = MainTable.query.all()
    return render_template('main_table/view_main_table.html', records=records)

@main_table_bp.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        sub_category_id = request.form['sub_category_id']
        payment_method_id = request.form['payment_method_id']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        value = request.form['value']
        description = request.form['description']
        date_added = datetime.now().date()
        
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            date = datetime(year, month, day).date()
        except ValueError:
            flash("Invalid date provided.")
            return redirect(url_for('main_table.add_record'))
        
        # Retrieve related objects from the database
        user = User.query.get(user_id)
        category = Category.query.get(category_id)
        sub_category = SubCategory.query.get(sub_category_id)
        payment_method = PaymentMethod.query.get(payment_method_id)

        # Validate that the IDs correspond to existing records
        if not user:
            flash("Invalid user ID.")
            return redirect(url_for('add_record'))
        if not category:
            flash("Invalid category ID.")
            return redirect(url_for('add_record'))
        if not sub_category:
            flash("Invalid sub-category ID.")
            return redirect(url_for('add_record'))
        if not payment_method:
            flash("Invalid payment method ID.")
            return redirect(url_for('add_record'))

        # Validate that the sub-category belongs to the category
        if sub_category.category_id != category.category_id:
            flash("Category ID does not match SubCategory's Category ID.")
            return redirect(url_for('main_table.add_record'))
        
        new_record = MainTable(
            user_id=user_id,
            category_id=category_id,
            sub_category_id=sub_category_id,
            payment_method_id = payment_method_id,
            year=year,
            month=month,
            day=day,
            date_added=date_added,
            value=value,
            description=description
        )
        db.session.add(new_record)
        db.session.commit()
        flash("Record added successfully.")
        return redirect(url_for('main_table.view_main_table'))
    
    users = User.query.all()
    categories = Category.query.all()
    sub_categories = SubCategory.query.all()
    return render_template('main_table/add_main_table_record.html', users=users, categories=categories, sub_categories=sub_categories)

@main_table_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    record = db.session.query(MainTable).filter_by(record_id=record_id).one()
    if request.method == 'POST':
        record.user_id = request.form['user_id']
        record.category_id = request.form['category_id']
        record.sub_category_id = request.form['sub_category_id']
        record.payment_method_id = request.form['payment_method_id'] 
        record.year = request.form['year']
        record.month = request.form['month']
        record.day = request.form['day']
        record.value = request.form['value']
        record.description = request.form['description']  
        db.session.commit()
        return redirect(url_for('main_table.view_main_table'))

    users = db.session.query(User).all()
    categories = db.session.query(Category).all()
    sub_categories = db.session.query(SubCategory).all()
    payment_methods = db.session.query(PaymentMethod).filter_by(user_id=record.user_id).all()
    return render_template('main_table/edit_main_table_record.html', record=record, users=users, categories=categories, sub_categories=sub_categories, payment_methods=payment_methods)

@main_table_bp.route('/delete/<int:record_id>', methods=['GET', 'POST'])
def delete_record(record_id):
    record = db.session.query(MainTable).filter_by(record_id=record_id).one()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('main_table.view_main_table'))

@main_table_bp.route('/get_payment_methods/<int:user_id>', methods=['GET'])
def get_payment_methods(user_id):
    payment_methods = db.session.query(PaymentMethod).filter_by(user_id=user_id).all()
    methods_list = [{'payment_method_id': pm.payment_method_id, 'method_name': pm.method_name} for pm in payment_methods]
    return jsonify({'payment_methods': methods_list})