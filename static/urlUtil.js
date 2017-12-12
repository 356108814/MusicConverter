//url工具函数

//获取当前url参数值
function getParamVal(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null){
        return unescape(r[2]);
    }else{
        return '';
    } 
}

//替换url中的参数
function replaceParamVal(oldurl, name, value) {
    var re = eval('/('+ name +'=)([^&]*)/gi');
    return oldurl.replace(re, name + '=' + value);
}



