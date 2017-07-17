__author__ = 'ty'

from .import api
from flask import abort,jsonify
from ums.controller import GetOneUserController
from ums import app
# from authentication import auth
#
#
# @api.route("/user/<username>")
# # @auth.login_required
# def retrieveInfo(username=None):
#     control = GetOneUserController()
#     userList = control.getUserInfoByName(username)
#     if len(userList) == 0:
#         return jsonify({"error": "404 not found"})
#     else:
#         return control.infoToJson(userList)
#
#
# @api.route("/hello")
# def show():
#     return jsonify({"hello": "hello Paul"})
#
#
# @api.route("/test")
# def test():
#     return jsonify({"test": "OK"})
