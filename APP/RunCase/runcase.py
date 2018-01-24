# -*- coding:utf-8 -*-

# from caseclient import api_request
# from common.log import LogSignleton
# from common.jsonvalue import JsonValue
# import re
# import json
# from common.httpclient import HttpClient
# from generatecase import GenerateCase

from .caseclient import api_request
from .common.log import LogSignleton
from .common.jsonvalue import JsonValue
import re
import json
from .common.httpclient import HttpClient
from .generatecase import GenerateCase
import time
import sys
__author__ = 'rudolf_han'

class RunCase():
    # run_id 运行配置的 id
    def __init__(self, env_type, log_name, run_id=0, case_id=None):

        # api_ids_list, case_ids_json, run_model, 可以通过 run_id 进行获取

        self.env_type = env_type
        self.log_name = log_name
        self.run_id = run_id
        self.batch_num = None
        self.logger = LogSignleton(log_name)
        self.http = HttpClient()
        self.gc = GenerateCase()
        self.gc.config_parse()
        self.gc.setup_teardown_info()

        # self.parse_json = self.gc.parse_json  # 全局变量
        # 项目前后置条件

        self.pro_parse_json = self.gc.parse_json[env_type]  # 全局变量

        if run_id:
            self.gc.run_config(run_id)
            self.case_ids_json = self.gc.case_ids_json
            self.run_model = self.gc.run_model   # 运行模式
            self.api_ids_list = self.gc.api_ids_list
            self.project_id = self.gc.project_id
        else:
            if case_id:
                self.gc.case_info(case_id)
                self.case_ids_json = {self.gc.case_json['api_id']: [self.gc.case_json['case_id']]}
                self.run_model = '2'  # 运行模式
                self.api_ids_list = [self.gc.case_json['api_id']]
                self.project_id = self.gc.case_json['project_id']
            else:
                self.logger.error('run_id 为0 ,未设置运行用例')
                sys.exit()
        if self.project_id:
            self.gc.mysql_con(self.project_id, env_type.split('_')[1].strip())
        else:
            sys.exit()
        # self.pro_setup_teardown = self.gc.pro_setup_teardown[self.project_id]

        self.jv = JsonValue()

    def setup(self, setup_info, type):
        # type 1 项目, 2 接口 , 3 用例
        if type == 1:  #  项目前置只支持sql
            self.gc.mysql_conn.execute_other(setup_info)
        elif type in (2, 3):
            if setup_info['setup']:  # 目前前置 只支持 sql 与前置用例
                self.gc.mysql_conn.execute_other(setup_info['setup'][0])
            if setup_info['rely_id']:
                api_id = self.gc.get_api_id(setup_info['rely_id'][0])
                # 查询数据 api_id, case_id
                self.api_run(api_id, setup_info['rely_id'][0])
            # 其余关键字形式
        # else:  # 用例前置
        #     if setup_info['setup']:  # 目前前置 只支持 sql 与前置用例
        #         self.gc.mysql_conn.execute_other(setup_info)
        #     if setup_info['rely_id']:
        #         api_id = self.gc.get_api_id(setup_info['rely_id'])
        #         # 查询数据 api_id, case_id
        #         self.api_run(api_id, setup_info['rely_id'])


    def tear_down(self, steardown_info):
        #if type == 1:  # 项目前置只支持sql
        # 后置目前只支持 sql 请环境
        if steardown_info['teardown']:
            self.gc.mysql_conn.execute_other(steardown_info['teardown'][0])
        # elif type in (2, 3):
        #     if setup_info['setup']:  # 目前前置 只支持 sql 与前置用例
        #         self.gc.mysql_conn.execute_other(setup_info)
        #     if setup_info['rely_id']:
        #         api_id = self.gc.get_api_id(setup_info['rely_id'])
        #         # 查询数据 api_id, case_id
        #         self.api_run(api_id, setup_info['rely_id'])

    def case_run(self, api_id, case_id):
        start = time.time()
        if case_id in self.gc.case_setup_teardown:
            case_setup_info = self.gc.case_setup_teardown[case_id]
            self.setup(case_setup_info)
        # 获取用例信息
        self.gc.case_info(case_id)
        self.api_method = self.gc.case_json['api_method']
        if 'http://' in self.gc.case_json['api_url']:
            requesr_url = self.gc.case_json['api_url']
        else:
            requesr_url = self.pro_parse_json['host'] + self.gc.case_json['api_url']
        #  组合 api_heard 新头部

        if self.gc.case_json['api_heard']:
            if (re.findall(r"#(.+?)#", self.gc.case_json['api_heard'])):
                param_names = (re.findall(r"#(.+?)#", self.gc.case_json['api_heard']))
                for param_name in param_names:
                    #  数据库中查询 中间结果值
                    self.gc.extract(self.env_type.split('_')[0], param_name)
                    if self.gc.extract_info:
                        api_head_new = self.gc.case_json['api_heard'].replace("#" + param_name + "#",
                                                                              self.gc.extract_info[0].strip())
                    else:
                        self.logger.error("中间变量：{0} 未获取到".format(param_name))
            else:
                api_head_new = self.gc.case_json['api_heard']
            api_head = dict(eval(self.pro_parse_json['head']), **eval(api_head_new))
        else:
            api_head = self.pro_parse_json['head']
        #  组合请求参数
        if self.gc.case_json['case_req']:
            if (re.findall(r"#(.+?)#", self.gc.case_json['case_req'])):
                param_names = (re.findall(r"#(.+?)#", self.gc.case_json['case_req']))
                for param_name in param_names:
                    # 数据库中查询 中间结果值
                    self.gc.extract(self.env_type.split('_')[0], param_name)
                    if self.gc.extract_info:
                        case_req_new = self.gc.case_json['case_req'].replace("#" + param_name + "#",
                                                                             self.gc.extract_info[0])
                    else:
                        self.logger.error("中间变量：{0} 未获取到".format(param_name))
            else:
                case_req_new = self.gc.case_json['case_req']

            if '{' in self.gc.case_json['case_req'] and '}' in self.gc.case_json['case_req']:
                # case_req = dict(eval(self.gc.case_json['api_req']), **eval(case_req_new))
                if self.gc.case_json['api_req']:
                    case_req = dict(eval(self.gc.case_json['api_req']), **eval(case_req_new))
                else:
                    case_req = eval(case_req_new)
            else:
                case_req = case_req_new
        else:
            case_req = self.gc.case_json['api_req']

        resp_result = api_request(self.http, requesr_url, api_head, case_req, self.api_method, self.logger)
        if self.gc.case_json['extract_failed']:
            for extratc_field in self.gc.case_json['extract_failed'].split('|'):
                para_name = extratc_field.split('=', 1)[0]
                if 'select' in extratc_field.split('=', 1)[1] or 'SELECT' in extratc_field.split('=', 1)[1]:
                    select_info = self.gc.mysql_conn.select_one_record(extratc_field.split('=', 1)[1])
                    para_value = list(select_info.values())[0]
                else:
                    path = extratc_field.split('=', 1)[1]
                    para_value = self.jv.get_result_value(resp_result, path)
                self.save_middle_result(para_name, para_value)

        # 断言 返回成功与 失败 与 失败原因
        __result, __reason = self.assert_result(resp_result, self.gc.case_json['expect_result'])
        endtimne = time.time()
        self.save_result(requesr_url, self.env_type.split('_')[0], api_id, case_id, api_head, case_req,
                         self.gc.case_json,
                         resp_result, __result, __reason, endtimne - start)
        #  用例层级的
        if case_id in self.gc.case_setup_teardown:
            case_setup_info = self.gc.case_setup_teardown[case_id]
            self.tear_down(case_setup_info)
    def api_run(self, api_id, case_id=None):
        # 接口前置条件
        if api_id in self.gc.api_setup_teardown:
            api_setup_info = self.gc.api_setup_teardown[api_id]
            self.setup(api_setup_info, 2)
        if case_id:
            self.case_run(api_id, case_id)
        else:
            for case_id in self.case_ids_json[api_id]:
                # 得到此用例，查看运行前置条件
                self.case_run(api_id, case_id)
        # 接口层的后置条件
        if api_id in self.gc.api_setup_teardown:
            api_setup_info = self.gc.api_setup_teardown[api_id]
            self.tear_down(api_setup_info)

    def run(self):
        self.gc.run_batch(self.run_id)
        self.batch_num = int(self.gc.run_batch_result[0]) + 1 if self.gc.run_batch_result[0] else 1
        # 项目前置条件运行
        if self.project_id in self.gc.pro_setup_teardown:
            pro_setup_info = self.gc.pro_setup_teardown[self.project_id]
            self.setup(pro_setup_info['setup'], 1)

        for api_id in self.api_ids_list:
            # 运行接口前置条件
            self.api_run(api_id)
        # if self.run_model == '2':  # 接口运行模式
        #     for api_id in self.api_ids_list:
        #         # 运行接口前置条件
        #         self.api_run(api_id)
        #
        # else:  # 用例运行模式 3
        #
        #     # 分组case
        #     print(self.case_ids_json)
        #     print(self.api_ids_list)
        #     # self.api_run('all')

        if self.project_id in self.gc.pro_setup_teardown:
            pro_setup_info = self.gc.pro_setup_teardown[self.project_id]
            self.tear_down(pro_setup_info)


    def assert_result(self, actual_value, expect_value):

        case_result, msg = self.jv.assert_value(actual_value, expect_value)
        if False in case_result:
            return 'fail', json.dumps(msg, indent=4, sort_keys=False, ensure_ascii=False)
        else:
            return 'success', ''


    def save_result(self, requesr_url, project_id, api_id, case_id, api_head, case_req, case_json, resp_result, run_result, result_reason, run_time):
        # 用例执行结果  默认保存
        if self.run_id:  # 当 run_id 不为 0 时 需要保存测试结果
            self.batch_num_num = self.batch_num
        #
        else:
            self.batch_num_num = -1

        insert_result = "insert into caseresult(project_id,api_id,case_id,project_name,api_name,case_name, \
                               head,method,params,respon,expect_result,run_result,result_reason,run_id,run_batch, request_url, run_time) \
                               VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}',{14},'{15}',{16})".format(
                project_id, api_id, case_id, case_json['pro_name'], case_json['api_name'], case_json['case_name'],
                api_head,
                case_json['api_method'], json.dumps(case_req, ensure_ascii=False),
                json.dumps(resp_result, ensure_ascii=False), case_json['expect_result'], run_result, result_reason,
                self.run_id, self.batch_num_num, requesr_url, run_time)
        self.gc.db_conn.execute_insert(insert_result)

    def save_middle_result(self, name, value):

        # 先查询 是否有相同的有的更新

        search_extract = " select count(1) from extract where project_id='{0}' and extract_field='{1}'".format(self.project_id, name)

        extract_count = self.gc.db_conn.select_one_record(search_extract)

        if extract_count[0] > 0:
            update_extract = " update extract set extract_value='{0}' where project_id='{1}' and extract_field='{2}' ".format(value, self.project_id, name)
            self.gc.db_conn.execute_update(update_extract)

        else:
            insert_extract = "insert into extract (project_id,extract_field,extract_value) values('{0}','{1}','{2}')".format(self.project_id, name, value)
            self.gc.db_conn.execute_insert(insert_extract)

# import datetime
# log_name =str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log'
# rc = RunCase('1_测试环境', log_name, 3)
# rc.run()


