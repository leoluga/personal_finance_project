from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)

    main_records = db.relationship('MainTable', back_populates='user')
    payment_methods = db.relationship('PaymentMethod', back_populates='user')

class PaymentMethod(db.Model):
    __tablename__ = 'payment_method'
    payment_method_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    method_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.user_id'), nullable=False)
    bank_name = db.Column(db.String)

    user = db.relationship('User', back_populates='payment_methods')
    main_records = db.relationship('MainTable', back_populates='payment_method')

class Category(db.Model):
    __tablename__ = 'category_table'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False, unique=True)

    sub_categories = db.relationship('SubCategory', back_populates='category')
    main_records = db.relationship('MainTable', back_populates='category')

class SubCategory(db.Model):
    __tablename__ = 'sub_category'
    sub_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub_category_name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_table.category_id'))

    category = db.relationship('Category', back_populates='sub_categories')
    main_records = db.relationship('MainTable', back_populates='sub_category')

class MainTable(db.Model):
    __tablename__ = 'main_table'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_table.category_id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.sub_category_id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.payment_method_id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer)
    date_added = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)

    user = db.relationship('User', back_populates='main_records')
    category = db.relationship('Category')
    sub_category = db.relationship('SubCategory', back_populates='main_records')
    payment_method = db.relationship('PaymentMethod', back_populates='main_records')
