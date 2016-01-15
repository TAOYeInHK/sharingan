/**
 * Created by ty on 2015/4/15.
 */
function onSearch(obj){
    setTimeout(function(){
        var storeId = document.getElementById('allUser');
        var rowsLength = storeId.rows.length;
        var key = obj.value;

        var searchCol = 0;
        var searchCol_2 = 1;

        for(var i=1;i<rowsLength;i++){
            var searchText = storeId.rows[i].cells[searchCol].innerText.toLowerCase();
            var searchText_2 = storeId.rows[i].cells[searchCol_2].innerText.toLowerCase();


            if(searchText.indexOf(key)!= -1 || searchText_2.indexOf(key) != -1){
                storeId.rows[i].style.display='';
            }else{
                storeId.rows[i].style.display='none';
            }
        }
    },200);
}