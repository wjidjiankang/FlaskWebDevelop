from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from models import User
from wtforms import ValidationError
from email_validator import validate_email, EmailNotValidError


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za_z][A-Za-z0-9_.]*$', 0,
                                                                                          'username must have only')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
        try:
            valid = validate_email(field.data)
            field.data = valid.email
        except EmailNotValidError:
            raise ValidationError('Please input correct email')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')