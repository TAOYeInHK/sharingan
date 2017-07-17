/**
 * Created by ty on 2015/4/30.
 */

function generatePwdView() {
    self.password = ko.observable();
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
    }
}

ko.applyBindings(new generatePwdView());