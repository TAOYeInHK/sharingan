# -*- coding:utf-8 -*-
__author__ = 'ty'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets import TextInput, PasswordInput


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()], widget=TextInput())
    password = PasswordField('password', validators=[DataRequired()], widget=PasswordInput())
