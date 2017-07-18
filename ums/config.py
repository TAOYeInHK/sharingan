# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.abspath(os.path.join(__file__, '..', '..'))


class BaseConfig(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'Qn5748h#UgLc1eR*0v'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/carbin' % BASE_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
