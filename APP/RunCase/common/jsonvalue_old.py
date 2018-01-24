# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from objectpath import *
import json
import sys
class JsonValue:
    def __init__(self):
        pass

    def __convert_json(self, value_str):
        
        if isinstance(value_str, str):
            
            self.__value_json = json.loads(value_str, encoding='utf-8')
            
        elif isinstance(value_str, dict):
            
            self.__value_json = value_str
            
        else:
            
            sys.exit()
    
    def get_result_value(self, result, path):
        """
        result : 输入值 \n
        
        path : 期望获取的值 path \n
        
        example : \n
        result: {"a":"b","b":["a","b",] , "c" :{"a":"b"} ,"d":{ "c":[1,2,3] } } \n
        except result : d - c 第二个值 , 注：从  0 开始 \n
        
        | ${x}= | get_result_value | result | d.c[2] | \n"
                  
        """
        
        # 转换 类型
        self.__convert_json(result) 
        try:
            result_value = Tree(self.__value_json).execute(path)
        except Exception as e:
            result_value = 'None'
            print(e)
        return result_value