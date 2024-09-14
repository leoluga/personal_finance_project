from flask import Flask

from personal_finance_app.routes.main_table import main_table_bp
from personal_finance_app.routes.categories import categories_bp
from personal_finance_app.routes.users import users_bp
from personal_finance_app.routes.payment_methods import payment_methods_bp

from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(main_table_bp, url_prefix='/main_table')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(payment_methods_bp, url_prefix='/payment_methods')

    return app