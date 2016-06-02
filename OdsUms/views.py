from flask import request, render_template, redirect, g, flash
from flask_login import login_required, logout_user, current_user

from . import app
from .controller import LoginController, AddUserController, GetAllUserController, UpdateUserController, GetOneUserController


@app.route('/', methods=['GET'])
def login_input():
    return render_template('/layout/login.html')


@app.route('/signin',methods=['POST'])
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
    user_collection = getUser.getUserInfo()
    return render_template('/layout/userList.html', name='hi', user_collection=user_collection)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.before_request
def before_request():
    g.user = current_user


@app.route("/userList/<int:user_id>", methods=['GET', 'POST'])
@login_required
def userBasicInfoEdit(user_id):
    if request.method == 'GET':
        getUser = GetOneUserController()
        user = getUser.getUserInfo(user_id)
        entitlement = getUser.getUserEntitlement(user_id)
        log = getUser.getLog(user_id)
        return render_template('/layout/editUser.html', userInfo=user,
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
            flash('Success!')
            return redirect('/userList')
        '''else:
            flash('Fail!')
            return redirect('/welcome/bad')'''


@app.route("/userList/addUser", methods=['GET', 'POST'])
@login_required
def addUser():
    if request.method == 'GET':
        return render_template('/layout/addUser.html')
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        memo = request.json['memo']
        expire_time = request.json['expire_time']
        add_user = AddUserController(username, password, memo, expire_time, g.user.user_id)
        if add_user.addUser():
            return "True"
        else:
            flash('Fail!')
            return redirect('/userList/addUser')