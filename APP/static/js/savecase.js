/**
 * Created by rudolf_han on 2017/4/18.
 */

//$(function() {
//    $('#btncase').click(function () {
//        var html = '';
//        var run_id=document.getElementById("run_api_id").innerText;
//        var api_id=document.getElementById("api_id").innerText;
//        var run_mode=document.getElementById("run_mode").innerText;
//        $('#history_income_list tr').find('td').each(function () {
//            if ($(this).index() == "0") { // 假设要获取第一列的值
//                html+=$(this).text()+','
//            }
//        });
//        $.ajax({
//        type: 'POST',
//        url: '/auth_option/savecase',
//        data: {case_ids:html, run_id:run_id, api_id:api_id, run_mode:run_mode}
//        })
//        .done(function(response) {
//                var json = eval("("+response+")");
//                //$('#successAlert').show();
//                //$('#msginfo_sucess').text(json.desc)
//				//$('#errorAlert').hide();.text(json.desc)
//
//			if (json.status =='ok') {
//                $('#successAlert').show();
//                $('#msginfo_sucess').text('保存成功！！！！！');
//			}
//            else{
//            $('#errorAlert').show();
//			$('#msginfo_error').text('保存失败,请重新操作！！！！')
//            }
//     });
//        });
//    });




    //    $.ajax({
    //    type: "POST",
    //    url: "/auth_option/savesort",
    //    data:{data: html, run_id:run_id},
    //    cache: false,
    //
    //    success: function(){
    //        alert("OK");
    //    }
    //});
