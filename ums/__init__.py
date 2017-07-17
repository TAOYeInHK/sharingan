# -*- coding:utf-8 -*-
__author__ = 'ty'
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.session_protection = 'strong'
app.config.from_object('OdsUms.config.BaseConfig')
db = SQLAlchemy(app)

import OdsUms.views
import forms
from .api import api as api_1_0_blueprint
app.register_blueprint(api_1_0_blueprint, url_prefix='/api')
