__author__ = 'ty'

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from passlib.handlers.pbkdf2 import pbkdf2_sha512
from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin
from OdsUms import db
import json

class Admin(db.Model, UserMixin):
    __tablename__='admin'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))
    apiKey = db.Column(db.String(100))

    def __init__(self, username, password, apiKey):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.apiKey = apiKey

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return super(User, self).__repr__()

class User(db.Model, UserMixin):
    __tablename__='user'
    user_id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))
    memo = db.Column(db.String(66000))
    expire_time = db.Column(db.Date)

    def __init__(self, username, password, memo, expire_time):
        self.username = username
        self.password = password
        self.memo = memo
        self.expire_time = expire_time

    def toJson(self):
        dic = {"user_id": self.user_id, "username": self.username,
               "password":self.password, "memo": self.memo,
               "expire_time": str(self.expire_time)}
        dicList = []
        dicList.append(dic)
        return dicList

class Entitlement(db.Model):
    __tablename__='entitlement'
    entitlement_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    #tentative
    entitlement = db.Column(db.String(10))

    def __init__(self, user_id, entitlement, start_time, end_time):
        self.user_id = user_id
        self.entitlement = entitlement
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return "symbol: "+ str(self.entitlement) + "  start: " + str(self.start_time) + "  end: " + str(self.end_time)

class Log(db.Model):
    __tablename__ = 'log'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    staff_id = db.Column(db.Integer)
    operation_type = db.Column(db.String(100))
    operation_time = db.Column(db.DateTime)
    data_field = db.Column(db.String(100))
    modification = db.Column(db.String(100))

    def __init__(self, user_id, staff_id, operation_time, operation_type, data_field, modification):
        self.user_id = user_id
        self.staff_id = staff_id
        self.modification = modification
        self.operation_time = operation_time
        self.operation_type = operation_type
        self.data_field = data_field