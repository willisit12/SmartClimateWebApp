# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ModelInputForm(FlaskForm):
    outside_temp = FloatField('Outside Temperature (°C)', validators=[
        DataRequired(),
        NumberRange(min=-50, max=50, message="Temperature must be between -50 and 50°C")
    ])
    room_temp = FloatField('Room Temperature (°C)', validators=[
        DataRequired(),
        NumberRange(min=-50, max=50, message="Temperature must be between -50 and 50°C")
    ])
    occupancy = IntegerField('Occupancy (Number of People)', validators=[
        DataRequired(),
        NumberRange(min=0, max=100, message="Occupancy must be between 0 and 100")
    ])
    hour_of_day = SelectField('Hour of the Day', choices=[(str(i), i) for i in range(24)], validators=[DataRequired()])
    weekday = SelectField('Day of the Week', choices=[
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ], validators=[DataRequired()])
    submit = SubmitField('Predict')
