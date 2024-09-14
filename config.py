import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personal_finance.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress the warning