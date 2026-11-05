from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first(): raise ValidationError('Username taken.')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first(): raise ValidationError('Email registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    overview = TextAreaField('Overview', validators=[DataRequired()])
    poster_path = StringField('Poster URL', validators=[Optional()])
    backdrop_path = StringField('Backdrop URL', validators=[Optional()])
    release_date = DateField('Release Date', format='%Y-%m-%d', validators=[Optional()])
    vote_average = FloatField('Rating (0-10)', validators=[Optional(), NumberRange(min=0, max=10)])
    trailer_url = StringField('Trailer URL', validators=[Optional()])
    submit = SubmitField('Save Movie')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(str(i), f'{i}/10') for i in range(1, 11)], validators=[DataRequired()])
    content = TextAreaField('Your Review', validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Submit Review')

# ─── فورم المسلسلات ───
class SeriesForm(FlaskForm):
    name = StringField('Series Name', validators=[DataRequired()])
    overview = TextAreaField('Overview', validators=[DataRequired()])
    poster_path = StringField('Poster URL', validators=[Optional()])
    backdrop_path = StringField('Backdrop URL', validators=[Optional()])
    first_air_date = DateField('First Air Date', format='%Y-%m-%d', validators=[Optional()])
    vote_average = FloatField('Rating (0-10)', validators=[Optional(), NumberRange(min=0, max=10)])
    trailer_url = StringField('Trailer URL', validators=[Optional()])
    submit = SubmitField('Save Series')
