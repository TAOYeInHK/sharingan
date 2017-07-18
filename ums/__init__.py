# -*- coding:utf-8 -*-
from flask import Flask
app = Flask(__name__)
app.config.from_object('ums.config.BaseConfig')

from ums import views
from ums import auth
