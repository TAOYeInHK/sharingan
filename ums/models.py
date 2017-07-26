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


class UserEntitlement(db.Model):
    __tablename__ = 'user_entitlement'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    entitlement_id = db.Column(db.Integer, db.ForeignKey('entitlement.id'), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user = db.relationship('User', back_populates='entitlements')
    entitlement = db.relationship('Entitlement', back_populates='users')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    memo = db.Column(db.String(1000))
    expire_time = db.Column(db.DateTime)
    entitlements = db.relationship(
        'UserEntitlement', back_populates='user'
    )

    def __init__(self, username, password, memo, expire_time):
        self.username = username
        self.password = password
        self.memo = memo
        self.expire_time = expire_time

    def __unicode__(self):
        return '[{}]{}'.format(self.id, self.username)

    def __str__(self):
        return '[{}]{}'.format(self.id, self.username)

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
    users = db.relationship(
        'UserEntitlement', back_populates='entitlement'
    )

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return '[{}]{}'.format(self.id, self.name)

    def __str__(self):
        return '[{}]{}'.format(self.id, self.name)


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
