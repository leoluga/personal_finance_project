from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Category, SubCategory

categories_bp = Blueprint('categories', __name__)

# View all categories
@categories_bp.route('/')
def view_categories():
    categories = Category.query.all()
    return render_template('categories/view_categories.html', categories=categories)

# View subcategories of a specific category
@categories_bp.route('/<int:category_id>')
def view_category_subcategories(category_id):
    category = Category.query.get_or_404(category_id)
    subcategories = SubCategory.query.filter_by(category_id=category_id).all()
    return render_template('categories/view_category_subcategories.html', category=category, subcategories=subcategories)

# Add a new category
@categories_bp.route('/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        existing_category = Category.query.filter_by(category_name=category_name).first()
        if existing_category:
            flash('Category already exists!', 'error')
            return redirect(url_for('categories.add_category'))
        
        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories.view_categories'))
    
    return render_template('categories/add_category.html')

# Delete a category
@categories_bp.route('/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories.view_categories'))

# Add a new subcategory to a specific category
@categories_bp.route('/<int:category_id>/add_subcategory', methods=['GET', 'POST'])
def add_subcategory(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        sub_category_name = request.form['sub_category_name']
        existing_sub_category = SubCategory.query.filter_by(sub_category_name=sub_category_name, category_id=category_id).first()
        if existing_sub_category:
            flash('Subcategory already exists in this category!', 'error')
            return redirect(url_for('categories.view_category_subcategories', category_id=category_id))
        
        new_sub_category = SubCategory(sub_category_name=sub_category_name, category_id=category_id)
        db.session.add(new_sub_category)
        db.session.commit()
        flash('Subcategory added successfully!', 'success')
        return redirect(url_for('categories.view_category_subcategories', category_id=category_id))
    
    return render_template('categories/add_subcategory.html', category=category)

# Edit a subcategory in a specific category
@categories_bp.route('/<int:category_id>/edit_subcategory/<int:sub_category_id>', methods=['GET', 'POST'])
def edit_subcategory(category_id, sub_category_id):
    subcategory = SubCategory.query.get_or_404(sub_category_id)
    if request.method == 'POST':
        subcategory.sub_category_name = request.form['sub_category_name']
        db.session.commit()
        flash('Subcategory updated successfully!', 'success')
        return redirect(url_for('categories.view_category_subcategories', category_id=category_id))
    
    return render_template('categories/edit_subcategory.html', category_id=category_id, subcategory=subcategory)

# Delete a subcategory in a specific category
@categories_bp.route('/<int:category_id>/delete_subcategory/<int:sub_category_id>', methods=['POST'])
def delete_subcategory(category_id, sub_category_id):
    subcategory = SubCategory.query.get_or_404(sub_category_id)
    db.session.delete(subcategory)
    db.session.commit()
    flash('Subcategory deleted successfully!', 'success')
    return redirect(url_for('categories.view_category_subcategories', category_id=category_id))