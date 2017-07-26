# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, FormField, FieldList
from wtforms.widgets import TextArea
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ums.models import Entitlement


class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')


class EntitlementForm(FlaskForm):
    name = StringField('产品名')


class RecordForm(FlaskForm):
    entitlement = QuerySelectField('产品名', query_factory=lambda: Entitlement.query, render_kw={
        'class': 'form-control'})
    start_time = DateTimeField('开始时间', render_kw={
        'class': 'form-control datetimeinput', 'type': 'datetime-local'})
    end_time = DateTimeField('结束时间', render_kw={
        'class': 'form-control datetimeinput', 'type': 'datetime-local'})


class UserForm(FlaskForm):
    username = StringField('客户姓名')
    password = PasswordField('客户密码')
    memo = StringField('备注', widget=TextArea())
    expire_time = DateTimeField('过期时间', format='%Y-%m-%dT%H:%M')
    record = FieldList(FormField(
        RecordForm, render_kw={'class': 'table table-bordered'}),
        label='产品详情', min_entries=1, max_entries=10,
        render_kw={'class': 'list-group'}
    )
