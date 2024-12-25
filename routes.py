# routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, Prediction
from forms import RegistrationForm, LoginForm, ModelInputForm
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ModelInputForm()
    prediction_results = None

    if form.validate_on_submit():
        # Retrieve form data
        try:
            outside_temp = float(form.outside_temp.data)
            room_temp = float(form.room_temp.data)
            occupancy = int(form.occupancy.data)
            hour_of_day = int(form.hour_of_day.data)
            weekday = int(form.weekday.data)
        except ValueError:
            flash('Invalid input. Please enter valid numbers.', 'danger')
            return render_template('dashboard.html', form=form, prediction_results=prediction_results)

        # Prepare input for models
        input_features = np.array([[outside_temp, room_temp, occupancy, hour_of_day, weekday]])

        # Make predictions using the loaded models
        ac_temp_model = current_app.ac_temp_model
        light_status_model = current_app.light_status_model

        if not ac_temp_model or not light_status_model:
            flash('Models are not loaded properly. Please contact the administrator.', 'danger')
            return render_template('dashboard.html', form=form, prediction_results=prediction_results)

        try:
            predicted_ac_temp = ac_temp_model.predict(input_features)[0]
            predicted_light_status = light_status_model.predict(input_features)[0]
        except Exception as e:
            flash(f'Error during prediction: {e}', 'danger')
            return render_template('dashboard.html', form=form, prediction_results=prediction_results)

        # Interpret light_status_pred if necessary (e.g., 0=Off, 1=On)
        light_status = 'On' if predicted_light_status == 1 else 'Off'

        # Round AC temperature prediction for readability
        predicted_ac_temp = round(predicted_ac_temp, 2)

        # Store the prediction in the database
        new_prediction = Prediction(
            outside_temp=outside_temp,
            room_temp=room_temp,
            occupancy=occupancy,
            hour_of_day=hour_of_day,
            weekday=weekday,
            predicted_ac_temp=predicted_ac_temp,
            predicted_light_status=light_status,
            user_id=current_user.id
        )
        db.session.add(new_prediction)
        db.session.commit()

        prediction_results = {
            'ac_temperature': predicted_ac_temp,
            'light_status': light_status
        }

        flash('Prediction successful and saved to your history!', 'success')

    return render_template('dashboard.html', form=form, prediction_results=prediction_results)
