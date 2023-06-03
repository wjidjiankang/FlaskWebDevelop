from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    email = StringField('Email')
    password = PasswordField('password', validators=[DataRequired(),])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')