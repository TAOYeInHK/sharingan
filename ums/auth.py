# -*- coding:utf-8 -*-
from flask import redirect
from flask_login import LoginManager

from ums import app
from ums.models import Admin


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id=admin_id).one()
