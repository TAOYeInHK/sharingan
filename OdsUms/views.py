# -*- coding:utf-8 -*-
from flask import request, render_template, redirect, g, flash
from flask_login import login_required, logout_user, current_user

from . import app
from .controller import LoginController, AddUserController, GetAllUserController, UpdateUserController, GetOneUserController


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET'])
def login_input():
    return render_template('/layout/login.html')


@app.route('/signin', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if LoginController.authenticate(username, password):
        return redirect("/userList")
    else:
        return redirect("/")


@app.route("/userList", methods=['GET'])
@login_required
def welcome():
    getUser = GetAllUserController()
    user_collection = getUser.get_user_list()
    return render_template('/layout/user_list.html', name='hi', user_collection=user_collection)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/userList/<int:user_id>", methods=['GET', 'POST'])
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


@app.route("/userList/addUser", methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('/layout/add.html')
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        memo = request.json['memo']
        expire_time = request.json['expire_time']
        add_user = AddUserController(username, password, memo, expire_time, g.user.user_id)
        try:
            add_user.add_user()
        except Exception:
            return "True"
        else:
            return redirect('/userList/addUser')