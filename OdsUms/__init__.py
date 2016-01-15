__author__ = 'ty'
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
lm = LoginManager()
lm.setup_app(app)
app.config.from_object('OdsUms.config.BaseConfig')
db = SQLAlchemy(app)

import OdsUms.views
import forms
from .api import api as api_1_0_blueprint
app.register_blueprint(api_1_0_blueprint, url_prefix='/api')