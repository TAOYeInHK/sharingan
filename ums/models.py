# -*- coding:utf-8 -*-
import datetime

from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin

from ums.database import db


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    api_key = db.Column(db.String(100), nullable=True)

    def __init__(self, username, password, apiKey):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.api_key = apiKey


records = db.Table(
    'records',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('entitle_id', db.Integer, db.ForeignKey('entitlement.id')),
    db.Column('start_time', db.DateTime),
    db.Column('end_time', db.DateTime),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    memo = db.Column(db.String(1000))
    expire_time = db.Column(db.DateTime)
    entitlements = db.relationship(
        'Entitlement', secondary=records,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username, password, memo, expire_time):
        self.username = username
        self.password = password
        self.memo = memo
        self.expire_time = expire_time

    def to_json(self):
        return [{
            'user_id': self.user_id, 'username': self.username,
            'password': self.password, 'memo': self.memo,
            'expire_time': str(self.expire_time),
        }]


class Entitlement(db.Model):
    __tablename__ = 'entitlement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, user_id, entitlement, start_time, end_time):
        self.user_id = user_id
        self.entitlement = entitlement
        self.start_time = start_time
        self.end_time = end_time


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    operation_type = db.Column(db.String(100))
    operation_time = db.Column(db.DateTime, default=datetime.datetime.now)
    data_field = db.Column(db.String(100))
    modification = db.Column(db.String(100))

    def __init__(self, user_id, admin_id, operation_type, data_field, modification):
        self.user_id = user_id
        self.admin_id = admin_id
        self.modification = modification
        self.operation_type = operation_type
        self.data_field = data_field
