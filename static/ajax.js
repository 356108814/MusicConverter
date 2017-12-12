/**
 * 客户端统一异步请求
 * Created by shiyong on 2015-12-14.
 */

$(function($){

    //老方式，页面表单提交
    $('.ajaxPost').click(function(){
		var target_form = $('#'+$(this).attr('target-form'));
        //验证通过，提交
        var validform = target_form.Validform();
        if(!validform.check()){
            return;
        }
        var url = target_form.attr('action');
        var jsonObject = target_form.serializeObject();
        $.ajax({
          type: 'POST',
          url: url,
          data: jsonObject,
          dataType: 'json',
          success: function(rdata){
              var time = 1500;
              //请求成功
              if (rdata.result == 'success') {
                //有跳转链接
                if (rdata.url) {
                    layer.msg(rdata.message + '，页面即将自动跳转~!',{icon:6, time:time});
                }else{
                    layer.msg(rdata.message,{icon:6, time:time});
                }
                setTimeout(function(){
                    if (rdata.url) {
                        location.href = rdata.url;
                    }else{
                        location.reload();
                    }
                },time);
            }else{
                layer.msg(rdata.message,{icon:5, time:time});
                setTimeout(function(){
                    if (rdata.url) {
                        location.href = rdata.url;
                    }
                },time);
            }
          }
        })
	});

    //弹出层模式的表单提交。成功先关闭弹出层，再刷新
    $('.ajaxButton').click(function(){
        var target_form = $('#'+$(this).attr('target-form'));
        //验证通过，提交
        var validform = target_form.Validform();
        if(!validform.check()){
            return;
        }
        var url = target_form.attr('action');
        var jsonObject = target_form.serializeObject();
        var opername = '保存';
        $.ajax({
          type: 'POST',
          url: url,
          data: jsonObject,
          dataType: 'json',
          success: function(rdata){
              var time = 1500;
              //请求成功
              if (rdata.success) {
                  // 成功回调url
                  var success_url = $('#success_url').val();
                  if (success_url != undefined && success_url != ''){
                      location.href = success_url;
                  }else{
                      layer.msg(opername + '成功',{icon:6, time:time});
                      // 先重新加载列表，再关闭
                      setTimeout(function(){
                          parent.location.reload();
                          var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                          parent.layer.close(index); //再执行关闭
                      },time);
                  }
              }else{
                  layer.msg(rdata.errmsg, {icon:5, time:time});
              }
          }
        })
	})
});

/**
 *获取url中的参数
 * @param param
 * @returns {*}
 */
function getParam(param) {
    var url = location.href;
    var rs = new RegExp("(^|)" + param + "=([^\&]*)(\&|$)", "gi").exec(url), tmp;
    if (tmp = rs) { return tmp[2]; }
    return "";
}

/**
 * 异步更新
 * @param url
 * @param jsonObject
 * @param successCallBack 请求成功回调函数
 * @param isReload 请求成功是否需要重新加载
 */
function ajaxUpdate(url,jsonObject,successCallBack,isReload){
    $.ajax({
      type: 'POST',
      url: url,
      dataType: 'json',
      data: jsonObject,
      success: function(rdata){
          var time = 1500;
          //请求成功
          if (rdata.result == 'success') {
            //有跳转链接
            if (rdata.url) {
                layer.msg(rdata.message + '，页面即将自动跳转~!',{icon:6, time:time});
            }else{
                if (rdata.message) {
                    layer.msg(rdata.message,{icon:6, time:time});
                }
            }
            //有回调函数
            if (successCallBack) {
                successCallBack(rdata.data)
            }
            setTimeout(function(){
                if (rdata.url) {
                    location.href = rdata.url;
                }else{
                    //处理加载
                    if(isReload === undefined){
                        isReload = true;
                    }
                    if(isReload == true){
                        location.reload();
                    }
                }
            },time);
        }else{
            layer.msg(rdata.message,{icon:5, time:time});
            setTimeout(function(){
                if (rdata.url) {
                    location.href = rdata.url;
                }
            },time);
        }
      }
    });
}

/**
 * 异步提交
 * @param url
 * @param jsonObject
 * @param successCallBack 请求成功回调函数
 */
function ajaxPost(url,jsonObject,successCallBack){
    $.ajax({
      type: 'POST',
      url: url,
      dataType: 'json',
      data: jsonObject,
      success: function(rdata){
          var time = 1500;
          //请求成功
          if (rdata.success) {
            //有回调函数
            if (successCallBack) {
                successCallBack(rdata.data)
            }
        }else{
            layer.msg(rdata['error_msg'], {icon:1,time:time});
        }
      }
    });
}

/**
 * 异步查询
 * @param url
 * @param jsonObject
 * @param successCallBack 请求成功回调函数
 */
function ajaxQuery(url,jsonObject,successCallBack){
    $.ajax({
      type: 'POST',
      url: url,
      dataType: 'json',
      data: jsonObject,
      success: function(rdata){
          var time = 1500;
          //请求成功
          if (rdata.result == 'success') {
            if(rdata.message){
              layer.msg(rdata.message,{icon:6,time:time});
            }
            //有回调函数
            if (successCallBack) {
                successCallBack(rdata.data)
            }
        }else{
            layer.msg(rdata.message,{icon:1,time:time});
            setTimeout(function(){
                if (rdata.url) {
                    location.href = rdata.url;
                }
            },time);
        }
      }
    });
}

/**
 * 异步请求
 * @param url
 * @param method GET、POST、PUT、DELETE
 * @param jsonObject
 * @param successCallBack 请求成功回调函数
 * @param isReload 请求成功是否需要重新加载
 */
function ajax(url,method,jsonObject,successCallBack,isReload){
    $.ajax({
      type: method,
      url: url,
      dataType: 'json',
      data: jsonObject,
      success: function(rdata){
          var time = 1500;
          //请求成功
          if (rdata.result == 'success') {
            //有跳转链接
            if (rdata.url) {
                layer.msg(rdata.message + '，页面即将自动跳转~!',{icon:6, time:time});
            }else{
                if (rdata.message) {
                    layer.msg(rdata.message,{icon:6, time:time});
                }
            }
            //有回调函数
            if (successCallBack) {
                successCallBack(rdata.data)
            }
            setTimeout(function(){
                if (rdata.url) {
                    location.href = rdata.url;
                }else{
                    //处理加载
                    if(isReload === undefined){
                        isReload = true;
                    }
                    if(isReload == true){
                        location.reload();
                    }
                }
            },time);
        }else{
            layer.msg(rdata.message,{icon:5, time:time});
            setTimeout(function(){
                if (rdata.url) {
                    location.href = rdata.url;
                }
            },time);
        }
      }
    });
}

/**
 * form表单序列化为json对象
 * @returns {{}}
 */
$.fn.serializeObject = function() {
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name] !== undefined) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
			//多选需要特殊处理
			if($('#'+this.name).attr('type') == 'multipleSelect'){
				var selectedArray = $('#'+this.name).multipleSelect('getSelects');
				var selected = ''
				for (var i = 0; i < selectedArray.length; i++) {
					selected += selectedArray[i];
					if(i != selectedArray.length - 1){
						selected += '、';
					}
				}
				o[this.name] = selected;
			}
		}
	});
	return o;
};

/**
 * 初始化验证表单。
 * @param formId
 * @param tiptype 提示类型
 */
function initValidForm(formId,tiptype){
    if(tiptype == undefined){
        tiptype = 4;
    }
    var form = $('#'+formId);
    //因为jQuery对象永远都有返回值
    if(form.length > 0){
        form.Validform({
            tiptype:tiptype,
            btnSubmit:".ajaxPost",
            callback:function(form){
                //验证通过不直接提交表单，而通过ajax自己处理
                return false;
            }
        });
    }
}
