__author__ = 'ty'
from flask_wtf import Form
from wtforms import BooleanField, StringField,PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    username = StringField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])


