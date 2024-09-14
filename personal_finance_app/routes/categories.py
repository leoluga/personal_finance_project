from flask import Blueprint, render_template, request, redirect, url_for
from models import Category, db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/')
def view_categories():
    categories = db.session.query(Category).all()
    return render_template('categories/categories.html', categories=categories)

@categories_bp.route('/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('categories.view_categories'))
    return render_template('categories/add_category.html')

@categories_bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = db.session.query(Category).filter_by(category_id=category_id).one()
    if request.method == 'POST':
        category.category_name = request.form['category_name']
        db.session.commit()
        return redirect(url_for('categories.view_categories'))
    return render_template('categories/edit_category.html', category=category)

@categories_bp.route('/delete/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = db.session.query(Category).filter_by(category_id=category_id).one()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.view_categories'))
