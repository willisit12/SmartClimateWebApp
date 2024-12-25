# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Smart_Climate_App'
    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///smart_climate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
