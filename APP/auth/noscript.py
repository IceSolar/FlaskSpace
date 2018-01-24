__author__ = 'rudolf_han'
# @auth_option.route('/runconfig/<int:run_id>', methods=['GET', 'POST'])
# def run_config_debug(run_id):
#     # case_ids = []
#     log_name = "_" + str(run_id) + "_" + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
#     try:
#         logs_info = []
#         run_debug(None, run_id, log_name, False)
#         logs_info = log_file(log_name, logs_info)
#         return jsonify({"respcode": '000', 'desc': '用例执行完成！！', 'log_info': logs_info})
#     except Exception as e:
#         logs_info = log_file(log_name)
#         logs_info.append(e)
#         return jsonify({"respcode": '999', 'desc': '用例执行失败！！', 'log_info': logs_info})

#
#
# @auth_option.route('/rundebug', methods=['GET', 'POST'])
# def run_debug_cases():
#     respon_json = {}
#     log_name = ''.join(eval(request.form['case_ids'])) + "_" + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
#     try:
#         logs_info = []
#         run_debug(eval(request.form['case_ids']), None, log_name, True)
#         logs_info = log_file(log_name, logs_info)
#         respon_json['status'] = 'ok'
#         respon_json['log_info'] = logs_info
#     except Exception as e:
#         logs_info = log_file(log_name)
#         logs_info.append(e)
#         respon_json['status'] = 'fail'
#         respon_json['log_info'] = logs_info
#     return json.dumps(respon_json)

