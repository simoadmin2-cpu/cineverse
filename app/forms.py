from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    overview = TextAreaField('Overview', validators=[DataRequired()])
    poster_path = StringField('Poster URL (e.g., https://image.tmdb.org/t/p/w500/...)', validators=[Optional()])
    backdrop_path = StringField('Backdrop URL', validators=[Optional()])
    release_date = DateField('Release Date', format='%Y-%m-%d', validators=[Optional()])
    vote_average = FloatField('Rating (0-10)', validators=[Optional(), NumberRange(min=0, max=10)])
    trailer_url = StringField('Trailer YouTube Link', validators=[Optional()])
    submit = SubmitField('Save Movie')
