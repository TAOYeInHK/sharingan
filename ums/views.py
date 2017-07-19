# -*- coding:utf-8 -*-

from passlib.apps import custom_app_context
from flask import request, render_template, redirect, g, flash, jsonify
from flask_login import login_required, logout_user, current_user, login_user

from ums import app
from ums.controller import UpdateUserController, GetOneUserController
from ums.database import session_scope
from ums.models import Admin, User
from ums.forms import LoginForm, RegistrationForm


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login_input():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('/layout/login.html', form=form)
    if not form.validate_on_submit():
        return redirect('/')
    admin = Admin.query.filter_by(username=form.username.data).first()
    if admin and custom_app_context.verify(
            secret=form.password.data, hash=admin.password):
        login_user(admin)
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('/layout/home.html')


@app.route('/user/list', methods=['GET'])
@login_required
def user_list():
    return render_template('/layout/list.html')


@app.route('/users/', methods=['GET'])
@login_required
def get_user_list():
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    with session_scope() as session:
        query = session.query(User)
        total = query.count()
        users = query.filter_by().limit(limit).offset(offset).all()

        return jsonify({'total': total, 'rows': [{
            'username': user.username,
            'expire_time': user.expire_time.strftime('%Y-%m-%d %H:%M'),
        } for user in users]})


@app.route("/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
def edit(user_id):
    if request.method == 'GET':
        getUser = GetOneUserController()
        user = getUser.get_user(user_id)
        entitlement = getUser.getUserEntitlement(user_id)
        log = getUser.getLog(user_id)
        return render_template('/layout/edit.html', userInfo=user,
                               entitlementInfo=entitlement, log=log)

    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]
        memo = request.json["memo"]
        expire_time = request.json['expire_time']
        modifiedEntitlement = request.json['modifiedEntitlement']
        deletedEntitlement = request.json['deletedEntitlement']
        update = UpdateUserController(user_id, g.user.user_id)
        if update.updateUserInfo(username, password, memo, expire_time, modifiedEntitlement, deletedEntitlement):
            return redirect('/userList')
        else:
            flash('Fail!')
            return redirect('/welcome/bad')


@app.route("/user/", methods=['GET', 'POST'])
@login_required
def add():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('/layout/add.html', form=form)
    if not form.validate_on_submit():
        return render_template('/layout/add.html', form=form)

    with session_scope() as session:
        user = User(
            username=form.username.data, password=form.password.data,
            memo=form.memo.data, expire_time=form.expire_time.data
        )
        session.add(user)
    return redirect('/')
