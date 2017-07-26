/**
 * Created by ty on 2015/5/4.
 */

$(function () {
   $('#records-add-row').click(function () {
       var $record_ul = $('#record');
       var $last_li = $($record_ul.children().slice(-1)[0]);
       var index = parseInt($('table', $last_li).attr('id').split('-')[1]);
       var $new_li = $last_li.clone();
       $record_ul.append($new_li);

   })
});

function addUserViewModel () {
    self.username = ko.observable("");
    self.password = ko.observable("");
    self.memo = ko.observable("");
    self.expire_time = ko.observable("");


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

    self.testValue = function() {
        alert(self.username() == null)
    };

    self.submit =function() {
        if (self.username() != "" && self.password() != "") {
        alert("operation success");
        var newUserData = {"username": self.username(), "password": self.password(), "memo": self.memo(), "expire_time":self.expire_time()};
        var data = JSON.stringify(newUserData);
        $.ajax({
            type: "POST",
            url : window.location.href,
            data : data,
            contentType: "application/json;charset=UTF-8",
            dataType : "json",
            success: function(data) {

                if(data.msg =="True" ){

                    alert("Success！");

                }else{

                    view(data.msg);

                }
            }


        });
        }else {
            alert("please fill in the username and password!")
        }

    }
}
ko.applyBindings(new addUserViewModel());