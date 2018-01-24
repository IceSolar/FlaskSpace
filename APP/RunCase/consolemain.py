# -*- coding:utf-8 -*-
__author__ = 'rudolf_han'
from .common.mydb import MyDb
from .common.httpclient import HttpClient
from .common.OptionParsArg import OptionArgs
from .generatecase import GenerateCase
from .common.log import LogSignleton
from config import *
import datetime
if __name__ == '__main__':
    # 命令行运行方式
    # 记录测试开始时间
    start_time = datetime.datetime.now()
    # 全局配置
    http = HttpClient()  # http
    db_conn = MyDb(db_path, 'sqlite')  # 用例库
    # 获取数据库配置
    # db2_conn = MyDb('', 'mysql')  # 项目库用于查询期望结果 ,数据库连接来源 sqlite 里的配置
    options, args = OptionArgs()

    if options.run:
        run_id = options.run
        logger = LogSignleton(run_id + "_" + str(datetime.datetime.now().strftime('%y%m%d%H%M%S')) + '.log')
        GenerateCase(db_conn, http, logger, run_id)
    else:
        print('传入参数失败，-h 查看帮助')

    # 获取配置 确定运行方式 (参数方式传入)



    # hc=HttpClient()
    # db =MyDb('../QADB.sqlite', 'sqlite')
    # sql_1 = 'select case_name  from apicase where id = 1'
    # result = db.select_one_record(sql_1)
    # print(result)
    # sql_2 = "SELECT * FROM apicase WHERE id = ? "
    # result2 = db.select_one_record(sql_2, '2')
    # print(result2)