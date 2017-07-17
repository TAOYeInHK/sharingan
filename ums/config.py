# -*- coding:utf-8 -*-
__author__ = 'ty'


class BaseConfig(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://root:12345678@localhost:3306/test'
