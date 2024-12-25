# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import pickle
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'  # Redirect to 'login' when login is required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models import User, Prediction
        db.create_all()

    # Load machine learning models
    artifacts_path = os.path.join(app.root_path, 'ml/model')
    temp_model_path = os.path.join(artifacts_path, 'ac_temperature_regressor.pkl')
    light_model_path = os.path.join(artifacts_path, 'light_status_classifier.pkl')

    try:
        with open(temp_model_path, 'rb') as temp_model_file:
            app.ac_temp_model = pickle.load(temp_model_file)
    except Exception as e:
        print(f"Error loading AC Temperature Model: {e}")
        app.ac_temp_model = None

    try:
        with open(light_model_path, 'rb') as light_model_file:
            app.light_status_model = pickle.load(light_model_file)
    except Exception as e:
        print(f"Error loading Light Status Model: {e}")
        app.light_status_model = None

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
