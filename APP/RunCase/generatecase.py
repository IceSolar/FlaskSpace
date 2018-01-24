# -*- coding:utf-8 -*-

import datetime
from .common.mydb import MyDb
# from common.mydb import MyDb
from config import *


__author__ = 'rudolf'

class GenerateCase():
    def __init__(self):
        self.start_time = datetime.datetime.now()
        # 全局配置
        # self.logger = LogSignleton(log_name)
        # self.http = HttpClient()  # http
        self.db_conn = MyDb(db_path, 'sqlite')  # 用例库
        # self.setup_teardown = {}  # 项目前后置条件
        self.pro_setup_teardown = {}
        self.api_setup_teardown = {}
        self.case_setup_teardown = {}
        self.the_belong = ['1', '2', '3']
        self.parse_json = {}  # 全局变量参数
        self.case_json = {}
        self.extract_info = []
        self.run_batch_result = None

        self.run_model = 0
        self.api_ids_list = []
        self.case_ids_json = {}
        self.project_id = None
        self.mysql_conn = None

    def mysql_con(self, project_id, env_name):
        # host, username, password, db, port
        db_info_sql = "select value from configparse where project_id = '{0}' and name = 'db' and config_name='{1}' ".format(project_id, env_name)
        db_info_mysql = self.db_conn.select_one_record(db_info_sql)
        if db_info_mysql:
            self.mysql_conn = MyDb(db_info_mysql[0], 'mysql')

    def config_parse(self):  # 全局变量的获取
        group_config = " select project_id, config_name from configparse group by project_id, config_name  "  # 主要是为了做环境区分
        group_config_infos = self.db_conn.select_many_record(group_config)
        for group_config_info in group_config_infos:
            config_infos_sql = " select name, value from configparse WHERE project_id ='{0}' and config_name ='{1}' ".format(group_config_info[0],group_config_info[1])
            config_infos = self.db_conn.select_many_record(config_infos_sql)
            __config_parse = {}
            for config_info in config_infos:
                __config_parse[config_info[0]] = config_info[1]
            self.parse_json[group_config_info[0]+'_'+group_config_info[1]] = __config_parse
    def setup_teardown_info(self):  # 前后置条件
        group_setup_teardown = "select the_belong, setup_teardown_id from setupteardown group by the_belong, setup_teardown_id"
        group_setup_teardown_infos = self.db_conn.select_many_record(group_setup_teardown)
        for group_setup_teardown_info in group_setup_teardown_infos:
            setup_teardown_sql = "select rely_id,setup_pro,teardown_pro from setupteardown where the_belong='{0}' and setup_teardown_id='{1}'".format(group_setup_teardown_info[0], group_setup_teardown_info[1])
            setup_teardown_infos = self.db_conn.select_many_record(setup_teardown_sql)
            setup_teardown = {}
            rely_id = []
            setup = []
            teardown = []
            for setup_teardown_info in setup_teardown_infos:
                if setup_teardown_info[0] != '-1':
                    rely_id.append(setup_teardown_info[0])
                if setup_teardown_info[1]:
                    setup.append(setup_teardown_info[1])
                if setup_teardown_info[2]:
                    teardown.append(setup_teardown_info[2])
            setup_teardown['rely_id'] = rely_id
            setup_teardown['setup'] = setup
            setup_teardown['teardown'] = teardown

            if group_setup_teardown_info[0] == '1':
                self.pro_setup_teardown[group_setup_teardown_info[1]] = setup_teardown
            elif group_setup_teardown_info[0] == '2':
                self.api_setup_teardown[group_setup_teardown_info[1]] = setup_teardown
            else:
                self.case_setup_teardown[group_setup_teardown_info[1]] = setup_teardown
    def get_api_id(self, case_id):

        get_api_id_sql = "select api_id from apicase   where id = '{0}'".format(case_id)
        __api_id = self.db_conn.select_one_record(get_api_id_sql)
        return __api_id[0]

    def case_info(self, case_id):    # 测试用例组合 (不包含前置用例)

        case_info_sql = "select c.name,b.api_name, b.api_url, b.api_heard, b.api_method, b.api_req, b.api_resp, \
               a.case_name, a.case_req, a.expect_result, a.Extract_failed , c.id, b.id, a.id \
                from apicase a inner join projectapis b on a.api_id = b.id \
                inner join projects c on b.project_id = c.id \
                where b.api_status = 'true' and a.case_status = 'true' and c.project_status = 'true' and  a.id = '{0}'".format(case_id)
        __case = self.db_conn.select_one_record(case_info_sql)
        if __case:
            self.case_json['pro_name'] = __case[0]
            self.case_json['api_name'] = __case[1]
            self.case_json['api_url'] = __case[2]
            self.case_json['api_heard'] = __case[3]
            self.case_json['api_method'] = __case[4]
            self.case_json['api_req'] = __case[5]
            self.case_json['api_resp'] = __case[6]
            self.case_json['case_name'] = __case[7]
            self.case_json['case_req'] = __case[8]
            self.case_json['expect_result'] = __case[9]
            self.case_json['extract_failed'] = __case[10]
            self.case_json['project_id'] = str(__case[11])
            self.case_json['api_id'] = str(__case[12])
            self.case_json['case_id'] = str(__case[13])

    def extract(self, project_id, name):

        extract_sql = "select extract_value from extract where project_id ='{0}' and extract_field='{1}' ".format(project_id, name)

        self.extract_info = self.db_conn.select_one_record(extract_sql)

    def insert_extract(self, project_id, name, value):

        insert_extract_sql = "insert into extract (project_id,extract_field,extract_value) values('{0}','{1}','{2}')".format(project_id, name, value)
        self.db_conn.execute_insert(insert_extract_sql)


    def run_batch(self, run_id):
        sql_run_batch = "select max(run_batch)  from caseresult where run_id = '{run_id}' ".format(run_id=run_id)
        self.run_batch_result = self.db_conn.select_one_record(sql_run_batch)


    def run_config(self, run_id):
        sql_run_config = "select project_id,run_mode,sort_id  from runcaseconfig where id= {run_id} ".format(run_id=run_id)
        run_config_info = self.db_conn.select_one_record(sql_run_config)
        self.run_model = run_config_info[1]
        self.project_id = run_config_info[0]
        if run_config_info[1] == '2':
            self.api_ids_list = run_config_info[2].split(',')
            for api_id in self.api_ids_list:
                case_sort_sql = " select case_id  from casesortconfig where run_config_id='{0}' and  api_id ='{1}'".format(run_id, api_id)
                case_sort = self.db_conn.select_one_record(case_sort_sql)
                # 如果只配置了 接口 没有配置用例顺序 需要处理
                if case_sort:
                    self.case_ids_json[api_id] = case_sort[0].split(',')
                else:
                    # 查询接口下的所有 用例 用例的顺序为 添加的顺序
                    case_ids_sql = " select id  from APICase where api_id ='{0}'".format(api_id)
                    case_ids = self.db_conn.select_many_record(case_ids_sql)
                    case_id_list = []
                    for case_id in case_ids:
                        case_id_list.append(str(case_id[0]))
                    self.case_ids_json[api_id] = case_id_list

        else:
            # 用例分组
            api_id_case = []
            case_ids_json_new = {}
            case_ids = run_config_info[2].split(',')
            for case_id in case_ids:
                api_id = self.get_api_id(int(case_id))
                if api_id not in api_id_case:
                    api_id_case.append(api_id)
                    case_ids_json_new[api_id] = [case_id]
                else:
                    case_ids_json_new[api_id].append(case_id)
            self.case_ids_json = case_ids_json_new

            self.api_ids_list = api_id_case

            # self.case_ids_json['all'] = run_config_info[2].split(',')

# gc = GenerateCase()
# gc.config_parse()
# gc.setup_teardown_info()
# gc.case_info('1')
# print(gc.parse_json)
# print(gc.api_setup_teardown)
# print(gc.pro_setup_teardown)
# print(gc.case_setup_teardown)
# print(gc.case_json)


