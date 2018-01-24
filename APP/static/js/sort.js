/**
 * Created by rudolf_han on 2017/4/19.
 */
$(document).ready(function () {
    $('#select-all').click(function () {
        if ($(this).prop('checked')) {
            $('.op_check').prop('checked', true);
        } else {
            $('.op_check').prop('checked', false);
        }
    });
});

$(document).ready(function() {//页面加载的时候触发
var boxObj = $("input:checkbox[name='sortcase']"); //获取所有的复选框值
    var expresslist = document.getElementById("cases_ids").innerText;; //用el表达式获取在控制层存放的复选框的值为字符串类型
    var express = expresslist.split(',');

    $.each(express, function(index, expressId){
       boxObj.each(function () {
            if($(this).val() == expressId.trim()) {
               $(this).attr("checked",true);
            }
        });
    });
});


//$(document).ready(function() {//页面加载的时候触发
//var boxObj = $("input:checkbox[name='sortapi']"); //获取所有的复选框值
//    var expresslist = document.getElementById("apis_ids").innerText;; //用el表达式获取在控制层存放的复选框的值为字符串类型
//    var express = expresslist.split(',');
//    alert(express)
//    $.each(express, function(index, expressId){
//       boxObj.each(function () {
//            if($(this).val() == expressId.trim()) {
//               $(this).attr("checked",true);
//            }
//        });
//    });
//});



//JS For select articles to delete (document).ready
$(function () {
    $('#addsortapi').click(function(){
        $('#addapiForm').submit();
    });

    $('#addsortapi').click(function () {

        if ($('.op_check').filter(':checked').size() > 0) {
            var apiIds = [];
            $('.op_check:checked').each(function(){
                apiIds.push($(this).val());
            });
            var apiIdsJson = JSON.stringify(apiIds);
            $('#api_ids').val(apiIdsJson);
        var run_id=document.getElementById("run_api_id").innerText;
            $.ajax({
        type: 'POST',
        url: '/auth_option/add_api',
        data: {api_ids:apiIdsJson,run_id:run_id}
        })
        .done(function(response) {
                var json = eval("("+response+")");
                //$('#successAlert').show();
                //$('#msginfo_sucess').text(json.desc)
				//$('#errorAlert').hide();.text(json.desc)

			if (json.status =='ok') {
                //$('#successAlert').show();
                //$('#msginfo_sucess').text('保存成功！！！！！');
                alert("保存成功！！！！！")
			}
            else{
            //$('#errorAlert').show();
			//$('#msginfo_error').text('保存失败,请重新操作！！！！')
                alert("保存失败,请重新操作！！！！")
            }
     })

        } else {
            alert("未选择任何接口！！")
        }

    });
});



function check(t,oper){
        var data_tr=$(t).parent().parent(); //获取到触发的tr
            if(oper=="MoveUp"){    //向上移动
               if($(data_tr).prev().html()==null){ //获取tr的前一个相同等级的元素是否为空
                   alert("已经是最顶部了!");
                   return;
               }{
                    $(data_tr).insertBefore($(data_tr).prev()); //将本身插入到目标tr的前面
               }
               }else{
                     if($(data_tr).next().html()==null){
                     alert("已经是最低部了!");
                     return;
                 }{
                      $(data_tr).insertAfter($(data_tr).next()); //将本身插入到目标tr的后面
                 }
               }
    }



$(document).ready(function () {
    $('#addsortcase').click(function(){
        $('#addcaseForm').submit();
    });

    $('#addsortcase').click(function () {

        if ($('.op_check').filter(':checked').size() > 0) {
            var caseIds = [];
            $('.op_check:checked').each(function(){
                caseIds.push($(this).val());
            });
            var caseIdsJson = JSON.stringify(caseIds);
            $('#case_ids').val(caseIdsJson);
        var run_id=document.getElementById("run_id").innerText;
        var api_id=document.getElementById("api_id").innerText;
        var run_mode=document.getElementById("run_mode").innerText;
        $.ajax({
        type: 'POST',
        url: '/auth_option/savecase',
        data: {case_ids:caseIdsJson,run_id:run_id, api_id:api_id,run_mode:run_mode}
        })
        .done(function(response) {
                var json = eval("("+response+")");
                //$('#successAlert').show();
                //$('#msginfo_sucess').text(json.desc)
				//$('#errorAlert').hide();.text(json.desc)

			if (json.status =='ok') {
                //$('#successAlert').show();
                //$('#msginfo_sucess').text('保存成功！！！！！');
                 alert("保存成功！！！！！")
			}
            else{
            //$('#errorAlert').show();
			//$('#msginfo_error').text('保存失败,请重新操作！！！！')
                alert("保存失败,请重新操作！！！！")
            }
     });
        } else {
            alert("未选择任何用例！！")
        }

    });
});




$(document).ready(function () {
    $('#rundebugcase').click(function(){
        $('#rundebugForm').submit();
    });
    $('#rundebugcase').click(function () {

        if ($('.op_check').filter(':checked').size() > 0) {
            var caseIds = [];
            $('.op_check:checked').each(function(){
                caseIds.push($(this).val());
            });
            var caseIdsJson = JSON.stringify(caseIds);
            $('#case_ids').val(caseIdsJson);
        //var run_id=document.getElementById("run_id").innerText;
        //var api_id=document.getElementById("api_id").innerText;
        //var run_mode=document.getElementById("run_mode").innerText;

        $.ajax({
        type: 'POST',
        url: '/auth_option/rundebug',
        data: {case_ids:caseIdsJson}
        })
        .done(function(response) {
                var json = eval("("+response+")");
                //$('#successAlert').show();
                //$('#msginfo_sucess').text(json.desc)
				//$('#errorAlert').hide();.text(json.desc)
        var html = '';
        var arr = json.log_info;
        for(var i=0;i<arr.length;i++){
        html +=arr[i]
        //alert(arr[i]);
        }
                alert(html)
        //document.getElementById('addloginfo').innerHTML = html;

            //if (json.status =='ok') {
            //    //$('#successAlert').show();
            //    //$('#msginfo_sucess').text('保存成功！！！！！');
            //     alert("保存成功！！！！！")
            //}
            //else{
            ////$('#errorAlert').show();
            ////$('#msginfo_error').text('保存失败,请重新操作！！！！')
            //    alert("保存失败,请重新操作！！！！")
            //}
     });
        } else {

            alert("未选择任何用例！！")
        }
    });
});


