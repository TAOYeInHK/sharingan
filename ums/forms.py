# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')


class RegistrationForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    memo = StringField('备注', widget=TextArea())
    expire_time = DateTimeField('过期时间', format='%Y-%m-%dT%H:%M')
