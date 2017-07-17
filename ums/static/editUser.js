/**
 * Created by ty on 2015/4/1.
 */

function singleEntitlement(symbol, start_time, end_time, entitlement_id, status) {
    var self = this;
    self.symbol = ko.observable(symbol);
    if (start_time == "None") {
       self.start_time = ko.observable("");
    } else {
       self.start_time = ko.observable(start_time);
    }
    self.start_time.subscribe(function(newValue) {
        if(self.end_time() != "" && self.end_time() != "None" && self.end_time != null && newValue != "None" && newValue != "" && newValue != null && newValue>self.end_time()){
            alert("end date should be later than start date");
            self.start_time(start_time);
        }
    });
    if (end_time == "None") {
        self.end_time = ko.observable("");
    }else {
        self.end_time = ko.observable(end_time);
    }
    self.end_time.subscribe(function(newValue) {
        if(self.end_time() != "" && self.end_time() != "None" && self.end_time != null && newValue != "None" && newValue != "" && newValue != null && newValue>self.end_time()) {
            alert("end date should be later than start date");
            self.end_time(end_time);
        }
    });
    self.entitlement_id = ko.observable(entitlement_id);
    self.status = ko.observable(status);

    this.setStatus = function(newStatus) {
        self.status = newStatus;
    };
}

function entitlementViewModel() {
    var self = this;

    var entitlementInfo = eval(document.getElementById("entitlementInfo").innerHTML) ;
    var userInfo = eval(document.getElementById("userInfo").innerHTML);

    var theDate = new Date();
    var yyyy = theDate.getFullYear().toString();
    var MM = (theDate.getMonth()+1).toString();
    var dd = theDate.getDate().toString();

    var newDate = new Date();
    var newTime=newDate.getTime()+(365*24*60*60*1000);
    newDate.setTime(newTime);
    var newyyyy = newDate.getFullYear().toString();
    var newMM = (newDate.getMonth()+1).toString();
    var newdd = newDate.getDate().toString();
    //basic information of a user
    self.user_id = ko.observable(userInfo[0].user_id);
    if (userInfo[0].username == "None") {
        self.username = ko.observable("");
    } else {
        self.username = ko.observable(userInfo[0].username);
    }
    if (userInfo[0].password == "None") {
        self.password = ko.observable("");
    } else {
        self.password = ko.observable(userInfo[0].password);
    }
    if (userInfo[0].memo == "None") {
        self.memo = ko.observable("");
    } else {
        self.memo = ko.observable(userInfo[0].memo);
    }
    self.expire_time = ko.observable(userInfo[0].expire_time);

    self.entitlementArray = ko.observableArray([]);
    self.entitlementArrayDelete = ko.observableArray([]);

    //add new entitlement
    self.newSymbol = ko.observable();

    self.newStart = ko.observable(yyyy+"-"+(MM[1]?MM:"0"+MM[0])+"-"+(dd[1]?dd:"0"+dd[0]));
    if((theDate.getMonth()+1) == 2 && theDate.getDate() == 29) {
        self.newEnd = ko.observable(newyyyy+"-"+"02"+"-"+"28")
    }else {
        self.newEnd = ko.observable(newyyyy+"-"+(newMM[1]?newMM:"0"+newMM[0])+"-"+(newdd[1]?newdd:"0"+newdd[0]));
    }


    for(var item in entitlementInfo){
        self.entitlementArray.push(new singleEntitlement(entitlementInfo[item]["symbol"],
            entitlementInfo[item]["start_time"], entitlementInfo[item]["end_time"],
            entitlementInfo[item]["entitlement_id"], "updated"));
    }

    self.add = function(){
        self.entitlementArray.push(new singleEntitlement("","","","","insert"));
    };
    self.remove = function(single) {
        self.entitlementArray.remove(single);
        single.setStatus("delete");
        self.entitlementArrayDelete.push(single);
    };
    self.update = function() {
        self.entitlementArray.sort();
        self.val = ko.toJSON(self.entitlementArray);
        //alert(self.val);
    };

    self.addEntitlement = function() {
        var newSymbol = self.newSymbol();
        var newStart = self.newStart();
        var newEnd = self.newEnd();


        if (newStart == "" || newStart == null) {
            newStart = self.getCurrentDate()
        }
        if (newEnd == "" || newEnd == null) {
            newEnd = self.getNextYearDate()
        }

        if(newEnd !="" && newEnd < newStart) {
            alert("end date should later than start date");
        }

        else if (newSymbol == "") {
            alert("invalid entitlement! Symbol should not be null")
        } else {
            self.entitlementArray.push(new singleEntitlement(newSymbol,newStart,newEnd,"","insert"));
            self.newSymbol();
            self.newStart(self.getCurrentDate());
            self.newEnd(self.getNextYearDate());
        }

    };
    self.randomPassword = function () {
        var str = "";
        var arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
            'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for(var i= 0; i<16 ; i++) {
            var pos = Math.round(Math.random()*(arr.length-1));
            str += arr[pos];
        }
        self.password(str);
    };


    self.getCurrentDate = function() {
        var yyyy = theDate.getFullYear().toString();
        var MM = (theDate.getMonth()+1).toString();
        var dd = theDate.getDate().toString();
        return yyyy+"-"+(MM[1]?MM:"0"+MM[0])+"-"+(dd[1]?dd:"0"+dd[0]);
    };

    self.getNextYearDate = function() {
        var newDate=new Date();
        var newTime=newDate.getTime()+(365*24*60*60*1000);
		newDate.setTime(newTime);
        var yyyy = (newDate.getFullYear()).toString();
        var MM = (newDate.getMonth()+1).toString();
        var dd = newDate.getDate().toString();
        if(theDate.getFullYear()%4==0 && (theDate.getMonth()+1) == 2 && theDate.getDate() == 29) {
            return yyyy+"-"+"02"+"-"+"28"
        }
        else {
            return yyyy+"-"+(MM[1]?MM:"0"+MM[0])+"-"+(dd[1]?dd:"0"+dd[0])
        }



    };

    self.submit = function () {


        if (self.expire_time() == "None" || self.expire_time() == "" || self.expire_time() == null) {
            self.expire_time("");
        }
        if (self.username() == "None") {
            self.username("")
        }
        if (self.password() == "None") {
            self.password("")
        }
        if (self.memo() == "None") {
            self.memo("")
        }



        var returnData = {"username": self.username(), "password": self.password(),
            "memo": self.memo(), "expire_time": self.expire_time(),
            "modifiedEntitlement": ko.toJSON(self.entitlementArray.sort()),
            "deletedEntitlement" :ko.toJSON(self.entitlementArrayDelete)
        };

        var data = JSON.stringify(returnData);
        $.ajax({
            type: "POST",
            url : window.location.href,
            data : data,
            cache : false,
            contentType: "application/json;charset=UTF-8",
            dataType : "json",
            success: function(data) {

                if(data.msg =="true" ){

                    alert("Success！");



                }else{

                    view(data.msg);

                }

            }



        });
        alert("operation success");

    };

    self.cancel = function() {
        window.location.reload();
    }
}
ko.applyBindings(new entitlementViewModel());