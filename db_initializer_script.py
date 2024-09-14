from flask import Flask
from models import db, User, Category, SubCategory, PaymentMethod
from personal_finance_app import create_app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        # Create all the tables in the database
        db.create_all()

        # Check for existing users
        leo_user = User.query.filter_by(username='Leonardo').first()
        if not leo_user:
            leo_user = User(username='Leonardo')
            db.session.add(leo_user)

        melina_user = User.query.filter_by(username='Melina').first()
        if not melina_user:
            melina_user = User(username='Melina')
            db.session.add(melina_user)

        # Check for existing categories
        expense_category = Category.query.filter_by(category_name='Expense').first()
        if not expense_category:
            expense_category = Category(category_name='Expense')
            db.session.add(expense_category)

        # Check for existing subcategories
        groceries_sub_category = SubCategory.query.filter_by(sub_category_name='Groceries', category_id=expense_category.category_id).first()
        if not groceries_sub_category:
            groceries_sub_category = SubCategory(sub_category_name='Groceries', category=expense_category)
            db.session.add(groceries_sub_category)

        # Check for existing payment methods
        payment_method_1 = PaymentMethod.query.filter_by(method_name="Leo's Credit Card", user_id=leo_user.user_id).first()
        if not payment_method_1:
            payment_method_1 = PaymentMethod(method_name="Leo's Credit Card", user=leo_user, bank_name='Nubank')
            db.session.add(payment_method_1)

        payment_method_2 = PaymentMethod.query.filter_by(method_name="Lina Credit Card", user_id=melina_user.user_id).first()
        if not payment_method_2:
            payment_method_2 = PaymentMethod(method_name="Lina Credit Card", user=melina_user, bank_name='Nubank')
            db.session.add(payment_method_2)

        # Commit the changes
        db.session.commit()

        print("Database and initial data created successfully.")
