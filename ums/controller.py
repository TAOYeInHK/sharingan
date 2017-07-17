# -*- coding:utf-8 -*-
import re
import json
import time
import datetime

from flask_login import login_user
from passlib.apps import custom_app_context as pwd_context

from ums.database import db
from ums.models import Admin, User, Entitlement, Log


class LoginController(object):
    @classmethod
    def authenticate(cls, username, password):
        admin = Admin.query.filter_by(username=username).first()
        if admin is not None and pwd_context.verify(password, admin.password):
            login_user(admin)
            return True
        else:
            return False


class AddUserController(object):
    def __init__(self, username, password, memo, expire_time, staff_id):
        self.username = username
        self.password = password
        self.memo = memo
        self.expire_time = expire_time
        self.staff_id = staff_id

    def is_valid_username(self):
        username_pattern = r'^[a-zA-Z0-9@._-]{1,20}$'
        match = re.match(username_pattern, self.username)
        if match:
            return True
        else:
            return False

    def is_valid_password(self):
        password_pattern = r'^.{1,64}$'
        match = re.match(password_pattern,self.password)
        if match:
            return True
        else:
            return False

    def is_valid_memo(self):
        if len(self.memo) < 65535:
            return True
        else:
            return False

    def add_user(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if len(str(self.expire_time)) == 0:
            self.expire_time = None
        user = User(self.username, self.password, self.memo, self.expire_time)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=self.username).first()
        log = Log(user.user_id, self.staff_id, current_time, "CreateAccount", "", "")
        db.session.add(log)
        db.session.commit()


class GetAllUserController(object):

    @classmethod
    def get_user_list(cls):
        userCollection = []
        result = db.engine.execute('Select user.user_id, user.username, user.password, '
                                   'user.memo, user.expire_time, tempEntitle.NumOfEntitle '
                                   'From user left join ('
                                   'Select entitlement.user_id, count(entitlement.entitlement) '
                                   'as NumOfEntitle From entitlement w'
                                   'here entitlement.end_time>CURRENT_DATE() '
                                   'Group By entitlement.user_id) As '
                                   'tempEntitle on user.user_id=tempEntitle.user_id')

        for item in result:
            temp_collection =[]
            numOfEntitlement = 0
            if item.memo is None or item.memo == "":
                item.memo == "None"

            active_entitlement = Entitlement.query.order_by(Entitlement.entitlement).filter(Entitlement.user_id == item.user_id).all()
            for i in active_entitlement:
                if i.end_time is None:
                    temp_collection.append(i.entitlement)
                    numOfEntitlement += 1
                elif datetime.datetime.strptime(str(i.end_time), '%Y-%m-%d')+datetime.timedelta(days=1) > datetime.datetime.today() :
                    temp_collection.append(i.entitlement)
                    numOfEntitlement += 1
            string1 = ",".join(temp_collection)
            user_tuple = (item.user_id, item.username, item.password, item.memo, item.expire_time, numOfEntitlement, string1)

            userCollection.append(user_tuple)
        return userCollection


class GetOneUserController(object):

    def get_user(self, user_id):
        user = User.query.filter(User.user_id == user_id).first()
        return user.to_json()

    def getUserInfoByName(self, username):
        user = User.query.filter(User.username == username).all()
        userList =[]
        for item in user:
            userList.append(item)
        return userList

    def getUserEntitlement(self, user_id):
        entitlementCollection = []
        entitlement = Entitlement.query.filter(Entitlement.user_id == user_id).all()
        for item in entitlement:
            tempDic ={}
            tempDic["symbol"] = item.entitlement
            tempDic["start_time"] = str(item.start_time)
            tempDic["end_time"] = str(item.end_time)
            tempDic["entitlement_id"] = item.entitlement_id
            tempDic["user_id"] = item.user_id
            #tempTuple = (item.entitlement, item.start_time, item.end_time, item.entitlement_id, item.user_id)
            entitlementCollection.append(tempDic)
        return entitlementCollection

    def sendMsg(self, user_id):
        entitlementCollection = self.getUserEntitlement(user_id)
        sum = 0
        price = 500
        for item in entitlementCollection:
            if item["payment_status"] == False:
                pass

    def getLog(self, user_id):
        logCollection = []
        log = db.engine.execute('select log.user_id as "user_id" , '
                                'log.staff_id as "staff_id", '
                                'log.operation_time as "operation_time", l'
                                'og.operation_type as "operation_type", '
                                'log.modification as "modification", '
                                'admin.username as "username" from log, admin '
                                'where log.staff_id=admin.user_id and log.user_id=%s'%(user_id))

        #log = Log.query.filter(Log.user_id == user_id).join(Admin, Log.staff_id == Admin.user_id).all()
        for item in log:
            tempDic = {}
            tempDic["staff_id"] = item.staff_id
            tempDic["staff_name"] = item.username
            tempDic["operation_time"] = str(item.operation_time)
            tempDic["operation_type"] = item.operation_type
            tempDic["modification"] = item.modification
            logCollection.append(tempDic)
        return logCollection


    def infoToJson(self,userList):
        if isinstance(userList, list):
            jsonList=[]
            for item in userList:
                userDic={}
                userDic["username"] = item.username
                userDic["password"] = item.password
                userDic["expire_at"] = str(item.expire_time)
                userDic["entitlements"] = self.getUserEntitlement(item.user_id)
                jsonList.append(userDic)
            return json.dumps(jsonList)



class UpdateUserController(object):
    def __init__(self, user_id, staff_id=None):
        self.user_id = user_id
        self.staff_id = staff_id

    def updateUserInfo(self, username, password, memo, expire_time, modifiedEntitlement, deletedEntitlement):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        user = db.session.query(User).filter(User.user_id == self.user_id).first()
        if username == "":
            username = None
        if user.username != username:
            operation_type = "ChangeUsername"
            data_field = '{"old":%s , "new":%s}' % (user.username, username)
            modification = 'Username Changed: from %s to %s' % (user.username, username)
            log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
            db.session.add(log)
            db.session.commit()
        if password == "":
            password = None
        if user.password != password:
            operation_type = "ChangePassword"
            data_field = ""
            modification = ""
            log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
            db.session.add(log)
            db.session.commit()

        if memo == "":
            memo = None
        if user.memo != memo:
            operation_type = "ChangeMemo"
            data_field = '{"old":%s , "new":%s}' % (user.memo, memo)
            modification = 'Memo Changed from: %s to %s' % (user.memo, memo)
            log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
            db.session.add(log)
            db.session.commit()

        if str(expire_time) == "":
            expire_time = None
        if not(expire_time is None and user.expire_time is None) :
            if str(user.expire_time) != str(expire_time):
                operation_type = "ChangeExpireTime"
                data_field = '{"old":%s , "new":%s}' % (str(user.expire_time),str(expire_time))
                modification = 'Expire time Changed from: %s to %s' % (str(user.expire_time), str(expire_time))
                log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
                db.session.add(log)
                db.session.commit()

        db.session.query(User).filter(User.user_id == self.user_id).update({User.username: username, User.password: password,
                                                                            User.memo: memo, User.expire_time: expire_time})

        db.session.commit()
        for item in json.loads(modifiedEntitlement):
            if len(str(item["start_time"])) == 0:
                item["start_time"] = None
            if len(str(item["end_time"])) == 0:
                item["end_time"] = None
            if item["status"] == "updated":
                entitle = db.session.query(Entitlement).filter(Entitlement.entitlement_id == item["entitlement_id"]).first()

                if entitle.entitlement == item["symbol"] and str(entitle.start_time) == str(item["start_time"]) and str(entitle.end_time) == str(item["end_time"]):
                    pass
                else:

                    db.session.query(Entitlement).filter(Entitlement.entitlement_id == item["entitlement_id"]).update({Entitlement.start_time : item["start_time"],
                                                                                                                       Entitlement.end_time : item["end_time"],
                                                                                                                       Entitlement.entitlement : item["symbol"]})
                    db.session.commit()
                    db.session.close()
                    operation_type = "ChangeEntitlement"

                    data_field = '{"symbol":%s, "start":%s, "end":%s }' % (item["symbol"], str(item["start_time"]), str(item["end_time"]))
                    modification = 'Entitlement Changed:%s. Valid from %s to %s' % (item["symbol"], str(item["start_time"]), str(item["end_time"]))
                    log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
                    db.session.add(log)
                    db.session.commit()

            elif item["status"] == "insert":
                entitle = Entitlement(self.user_id, item["symbol"], item["start_time"], item["end_time"])
                db.session.add(entitle)
                db.session.commit()
                db.session.close()
                operation_type = "AddEntitlement"

                data_field = '{"symbol":%s, "start":%s, "end":%s }' % (item["symbol"], str(item["start_time"]), str(item["end_time"]))
                modification = 'Entitlement Added: %s. Valid from %s to %s' % (item["symbol"], str(item["start_time"]), str(item["end_time"]))
                log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
                db.session.add(log)
                db.session.commit()
            else:
                pass

        for item in json.loads(deletedEntitlement):
            if item["entitlement_id"] != "":
                db.session.query(Entitlement).filter(Entitlement.entitlement_id == item["entitlement_id"]).delete()
                db.session.commit()
                db.session.close()
                operation_type = "DeleteEntitlement"
                data_field = ""
                modification = "Entitlement Deleted: %s" % (str(item["symbol"]))
                log = Log(self.user_id, self.staff_id, current_time, operation_type, data_field, modification)
                db.session.add(log)
                db.session.commit()
        return True


# add new admin
def new_user(username, password, apiKey):
    user=Admin(username,password,apiKey)
    db.session.add(user)
    db.session.commit()
