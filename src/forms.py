from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    firstname = StringField('First name', validators=[DataRequired('Please enter your first name')])
    lastname = StringField('Last name', validators=[DataRequired('Please enter your last name')])
    email = StringField('Email', validators=[DataRequired('Valid Email address required'), Email('Must be a valid email address')])
    password = PasswordField('Password', validators=[DataRequired('Password is required'), Length(min=6, message='Password must be at least 6 characters long.')])
    submit = SubmitField('Sign up!')

class LoginForm(Form):
    email = StringField('Email Address', validators=[DataRequired('Valid Email address required'), Email('Email must be valid email address')])
    password = PasswordField('Password', validators=[DataRequired('Password required')])
    submit = SubmitField('Log in')

class AddressForm(Form):
    address = StringField('Address', validators=[DataRequired('Please enter an address')])
    submit = SubmitField('Search')

