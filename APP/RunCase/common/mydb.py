# -*- coding:utf-8 -*-
import sqlite3
import sys
import pymysql.cursors
__author__ = 'rudolf_han'
class MyDb():
    # 目前涉及到两种数据库类型 ： mysql, sqlite3
    def __init__(self, db_config, db_type):

        try:
            if 'sqlite' in db_type:
                self.dbconn = sqlite3.connect(db_config)
            elif 'mysql' in db_type:
                # db_config="host, username,password,db, port"
                db_config_info = db_config.split(',')

                # Connect to the database
                self.dbconn = pymysql.connect(host=db_config_info[0], user=db_config_info[1], password=db_config_info[2], db=db_config_info[3],
                                             port=int(db_config_info[4]), charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        except Exception as e:
            print('初始化数据连接失败：%s' % e)
            #logger.error('初始化数据连接失败：%s' % e)
            sys.exit()

    def get_conn(self):
        return self.dbconn

    def execute_other(self, query):
        #logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            print(e)
            #logger.error('执行数据库插入操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()



    def execute_insert(self, query, data=''):
        #logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            print(e)
            #logger.error('执行数据库插入操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()

    def execute_update(self, query):
        #logger.info('query：%s' % query)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            #logger.error('执行数据库更新操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()

    def select_one_record(self, query, data=""):
        '''返回结果只包含一条记录'''
        #logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:

                db_cursor.execute(query)
            query_result = db_cursor.fetchone()
            return query_result
        except Exception as e:
            print(e)
            #logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            exit()

    def select_many_record(self, query, data=""):
        '''返回结果只包含多条记录'''
        #logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            return query_result
        except Exception as e:
            #logger.error('执行数据库查询操作失败：%s' % e)
            print(e)
            db_cursor.close()
            exit()

    def close(self):
        self.dbconn.close

# db =MyDb('../../QADB.sqlite', 'sqlite')
# sql_1 = 'select case_name  from apicase where id = 1'
# result = db.select_one_record(sql_1)
# print(result)
# sql_2 = "SELECT * FROM apicase WHERE id = ? "
# result2 = db.select_one_record(sql_2, '2')
# print(result2)
#
# db_con ='192.168.21.22,root,We-are-hero-2015,jf_installment,3306'
# #'t.jufandev.com,root,We-are-hero-2015,asset_op,30621'
#
# db = MyDb(db_con, 'mysql')
# sql_1 = "SELECT SUBSTRING(content, 7, 4)  FROM t_sms_log WHERE mobile = '13621780941' AND sms_type ='1' ORDER BY send_time DESC LIMIT 1 "
# result = db.select_many_record(sql_1)
# print(list(result[0].values())[0])
# print(result[0].values())
