/**
 * Created by wuyan on 2017/4/12.
 */

var formatJson = function (json, options) {
        var reg = null,
                formatted = '',
                pad = 0,
                PADDING = '    ';
        options = options || {};
        options.newlineAfterColonIfBeforeBraceOrBracket = (options.newlineAfterColonIfBeforeBraceOrBracket === true) ? true : false;
        options.spaceAfterColon = (options.spaceAfterColon === false) ? false : true;
        if (typeof json !== 'string') {
            json = JSON.stringify(json);
        } else {
            json = JSON.parse(json);
            json = JSON.stringify(json);
        }
        reg = /([\{\}])/g;
        json = json.replace(reg, '\r\n$1\r\n');
        reg = /([\[\]])/g;
        json = json.replace(reg, '\r\n$1\r\n');
        reg = /(\,)/g;
        json = json.replace(reg, '$1\r\n');
        reg = /(\r\n\r\n)/g;
        json = json.replace(reg, '\r\n');
        reg = /\r\n\,/g;
        json = json.replace(reg, ',');
        if (!options.newlineAfterColonIfBeforeBraceOrBracket) {
            reg = /\:\r\n\{/g;
            json = json.replace(reg, ':{');
            reg = /\:\r\n\[/g;
            json = json.replace(reg, ':[');
        }
        if (options.spaceAfterColon) {
            reg = /\:/g;
            json = json.replace(reg, ':');
        }
        (json.split('\r\n')).forEach(function (node, index) {
                    var i = 0,
                            indent = 0,
                            padding = '';

                    if (node.match(/\{$/) || node.match(/\[$/)) {
                        indent = 1;
                    } else if (node.match(/\}/) || node.match(/\]/)) {
                        if (pad !== 0) {
                            pad -= 1;
                        }
                    } else {
                        indent = 0;
                    }

                    for (i = 0; i < pad; i++) {
                        padding += PADDING;
                    }

                    formatted += padding + node + '\r\n';
                    pad += indent;
                }
        );
        return formatted;
    };


function get_projectname_info(url) {
    $.getJSON(url, function(data) {
        $('#project_id').val(data.project_id);
        $('#project_id').hide();
        $('#modaladdapi').modal();
    });
}

function get_project_info(url) {
    $.getJSON(url, function(data) {
        $('#project_name4').val(data.project_name);
        $('#project_url4').val(data.project_url);
        $('#is_valid4').val(data.project_status);
        $('#project_remark4').val(data.project_remark);
        $('#project_id4').val(data.project_id);

        $(":radio[name='is_valid'][value='" + data.project_status + "']").prop("checked", "checked");

        $('#modaleditproject').modal();
    });
}

function change(){
     document.getElementById("sel")[2].selected=true;
}

function get_api_value(url) {
    $.getJSON(url, function(data) {
        $('#api_name4').val(data.api_name);
        $('#api_url4').val(data.api_url);
        $('#api_status4').val(data.api_status);
        $('#api_req4').val(data.api_req);
        $('#project_id4').val(data.project_id);
        $('#api_id4').val(data.api_id);
        $('#api_heard4').val(data.api_heard);
        $('#api_resp4').val(data.api_resp);
        $('#api_method4').val(data.api_method);

        $(":radio[name='api_valid'][value='" + data.api_status + "']").prop("checked", "checked");
        $('#Modaleditapi').modal();
    });
}

function get_case_value(url) {
    $.getJSON(url, function(data) {
        $('#case_id3').val(data.case_id);
        $('#case_name3').val(data.case_name);
        $('#case_desc3').val(data.case_desc);
        $('#rely_case_id3').val(data.rely_case_id);
        $('#api_id3').val(data.api_id);
        $('#project_id3').val(data.project_id);
        $('#case_req3').val(data.case_req);
        $('#case_head_add3').val(data.case_head_add);
        $('#expect_result3').val(data.expect_result);
        $('#Extract_failed3').val(data.Extract_failed);
        $('#case_valid3').val(data.case_valid);

        $(":radio[name='case_valid'][value='" + data.case_valid + "']").prop("checked", "checked");

        $('#ModaleditAPICase').modal();
    });
}




function get_case_info(url) {
    $.getJSON(url, function(data) {
        $('#api_name11').text(data.api_name);
        $('#case_name11').text(data.case_name);
        $('#case_url11').text(data.api_url);
        $('#case_headl11').text(data.api_heard);
        $('#case_method11').text(data.api_method);
        $('#case_req11').text( data.api_req);
        $('#case_resp11').append(data.api_resp);
        //document.getElementById('#case_resp11').innerHTML += ;
        $('#expect_result11').text(data.expect_result);
        $('#Extract_failed11').text(data.Extract_failed);




        //$('#case_req3').val(data.case_req);
        //$('#case_head_add3').val(data.case_head_add);
        //$('#expect_result3').val(data.expect_result);
        //$('#Extract_failed3').val(data.Extract_failed);
        //$('#case_valid3').val(data.case_valid);
        //
        //$(":radio[name='case_valid'][value='" + data.case_valid + "']").prop("checked", "checked");

        $('#APICaseValue').modal();
    });
}


function get_projecapi_id(url) {
    $.getJSON(url, function(data) {
        $('#project_id3').val(data.project_id);
        $('#api_id3').val(data.api_id);
        $('#project_id3').hide();
        $('#api_id3').hide();
        $('#addapicase').modal();
    });
}


function run_case_id(url) {
    $.getJSON(url, function(data) {

        var html = '';
        var arr = data.log_info;

        for(var i=0;i<arr.length;i++){
        html += '<li>'+arr[i]+'</li>'
        //alert(arr[i]);
        }
        document.getElementById('addloginfo').innerHTML = html;
        //$('#caselog').modal();
        //
        //alert(data.respcode + data.desc + data.reason)
    });
}



function run_config_id(url) {
    $.getJSON(url, function(data) {

        var html = '';
        var arr = data.log_info;

        for(var i=0;i<arr.length;i++){
        html += '<li>'+arr[i]+'</li>'
        //alert(arr[i]);
        }
        document.getElementById('addloginfo').innerHTML = html;
        $('#caselog').modal();
        //
        //alert(data.respcode + data.desc + data.reason)
    });
}

function get_config_info(url) {
    $.getJSON(url, function(data) {
        $('#run_id4').val(data.run_id);
        $('#project_id4').val(data.project_id);
        $('#plan_name4').val(data.plan_name);
        $('#run_time4').val(data.run_time);
        $('#run_mode4').val(data.run_mode);
        $(":radio[name='run_mode'][value='" + data.run_mode + "']").prop("checked", "checked");
        $('#config_status4').val(data.config_status);
        $(":radio[name='config_status'][value='" + data.config_status + "']").prop("checked", "checked");
        $('#modaleditconfig').modal();
    });
}


function get_parse_info(url) {
    $.getJSON(url, function(data) {
        $('#config_id3').val(data.config_id);
        $('#project_id3').val(data.project_id);
        $('#config_name3').val(data.config_name);
        $('#name3').val(data.name);
        $('#value3').val(data.value);
        //
        //$(":radio[name='is_valid'][value='" + data.project_status + "']").prop("checked", "checked");

        $('#modaleditconfig').modal();
    });
}

function get_setup_info(url) {
    $.getJSON(url, function(data) {
        $('#the_belong5').val(data.belong_id);
        $('#setup_teardown_id').val(data.setup_teardown_id);
        $('#project_id5').val(data.project_id);
        var anObject = data.rely_id_json;//对json数组each
        var html = '';
        $.each(anObject,function(name,value) {
            html += '<option value='+name+'>'+value+'</option>'
            //$("#relay_id5").append("<option value='"+name+">"+value+"</option>");
        });
        document.getElementById('relay_id5').innerHTML = html;

        $('#api_id5').val(data.api_id);
        $("#relay_id5 option[value='-1']").attr("selected", true);
        //$(":radio[name='is_valid'][value='" + data.project_status + "']").prop("checked", "checked");

        $('#addprosetup').modal();
    });
}


function edit_setup_info(url) {
    $.getJSON(url, function(data) {

        $('#SetupTearDown_id2').val(data.id);
        $('#the_belong2').val(data.the_belong);
        $('#setup_teardown_id').val(data.setup_teardown_id);
        $('#project_id5').val(data.project_id);
        //$('#setup_type2').val(data.setup_type);
        $('#setup_pro2').val(data.setup_pro);
        $('#teardown_pro2').val(data.teardown_pro);

        var anObject = data.rely_id_json;//对json数组each
        var html = '';
        $.each(anObject,function(name,value) {
            html += '<option value='+name+'>'+value+'</option>'
            //$("#relay_id5").append("<option value='"+name+">"+value+"</option>");
        });
        document.getElementById('relay_id2').innerHTML = html;

        //$('#api_id5').val(data.api_id);
        $("#relay_id2 option[value="+data.rely_id+"]").attr("selected", true);
        //$(":radio[name='is_valid'][value='" + data.project_status + "']").prop("checked", "checked");

        $('#editprosetup').modal();
    });
}