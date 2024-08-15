from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_adult = BooleanField('Hogflix in kid-friendly mode?')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangePlanForm(FlaskForm):
    plan = HiddenField('Plan')  # Remove DataRequired for debugging
    submit = SubmitField('Change Plan')


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')

    