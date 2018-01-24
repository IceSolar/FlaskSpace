# -*- coding:utf-8 -*-
__author__ = 'dellpc'
from objectpath import *
import json
class JsonValue():
    def __init__(self):
        self.path_list = []  # 获取json串中 所有key 的路径
        self.list_value_new = []  # 接收转换的 list
        self.__expect_json = {}
        self.__actual_json = {}


    def __get_json_path(self, value_info, key_path=''):
        if isinstance(value_info, dict):
            for k, v in value_info.items():
                if isinstance(v, (str, int, float, type(None))):
                    self.path_list.append(key_path+"."+k if key_path else k)
                else:
                    self.__get_json_path(v, key_path+"."+k if key_path else k)
        elif isinstance(value_info, list):
            self.path_list.append(key_path)
        return self.path_list
    def __get_list_path(self, value_info, key_path=''):
        # 获取 list中的数据的 path 路径
        self.path_list = []
        if isinstance(value_info, list):
            if self.__list_contents_dict(value_info):
                key_index = 0
                for value__ in value_info:
                    if isinstance(value__, dict):
                        self.__get_json_path(value__, key_path+str(key_index))
                    elif isinstance(value__, list):
                        self.__get_list_path(value__, key_path+str(key_index))
                    else:
                        continue
                    key_index = +1
        return self.path_list
    def __list_contents_dict(self, list_value):
        # 类型转换
        if isinstance(list_value, list):
            self.list_value_new = list_value
        elif isinstance(list_value, str) and list_value[0] == '[' and list_value[-1] == "]":
            self.list_value_new = eval(list_value)
        else:
            print('数据不符合转换为LIST')
            return False
        isdict_list = []
        # LIST 中只要存在一个 DICT 就返回True
        if self.list_value_new:
            for __list_value in self.list_value_new:
                if isinstance(__list_value, dict):
                    isdict_list.append(True)
                elif isinstance(__list_value, (list, tuple)):
                    self.__list_contents_dict(__list_value)
                else:
                    isdict_list.append(False)
        # 最终返回 结果
        if True in isdict_list:
            return True
        else:
            return False
    def __convert_json(self, value_str):

        if isinstance(value_str, str):
            convert_json_value = json.loads(value_str.replace('\\', ''), encoding='utf-8')
        elif isinstance(value_str, dict):
            convert_json_value = value_str
        else:
            print ("数据类型错误无法进行转换")
            sys.exit()
        return convert_json_value
    def __euqal_list_value(self, expect_value, actual_value, key_path=''):

        if isinstance(expect_value, list) and self.__list_contents_dict(expect_value):  # 判断list数据中是否有dict数据，有继续
            expect_value.sort(key=lambda obj: list(obj.items())[0])
            actual_value.sort(key=lambda obj: list(obj.items())[0])

            list_path_list = self.__get_list_path(expect_value)  # 获取list 中dict 中key的路径

            for j in list_path_list:

                expect_value_new = Tree(expect_value[int(j.split('.', 1)[0])]).execute("$."+j.split('.', 1)[1])
                actual_value_new = Tree(actual_value[int(j.split('.', 1)[0])]).execute("$."+j.split('.', 1)[1])

                if isinstance(expect_value_new, dict):  # 如果期望结果为dict 则调用 json 的比较

                    self.__euqal_json_value(expect_value_new, actual_value_new, key_path+'|'+j)

                elif isinstance(expect_value_new, (list, tuple)):  # 如果期望结果为list 则调用自己

                    if len(expect_value_new) == len(actual_value_new):
                        self.__euqal_list_value(expect_value_new, actual_value_new, key_path+'|'+j)

                    else:

                        self.msg[key_path+'|'+j] = '实际结果与期望结果的长度不一致（注：list 比较必须相同）'
                        self.assert_result.append(False)

                else:  # 不属于以上两种情况 直接调用比较方法
                    self.__equal_field(actual_value_new, expect_value_new, key_path+'|'+j)
        else:  # list 中数据 无 dict 格式数据
            expect_value.sort()
            actual_value.sort()
            if (len(expect_value) if expect_value else 0) == (len(actual_value) if expect_value else 0):
                for i in range(len(expect_value)):
                    if isinstance(expect_value[i], (list, tuple)) and expect_value and actual_value:
                        self.__euqal_list_value(expect_value[i], actual_value[i], key_path)
                    elif isinstance(expect_value[i], dict):
                        self.__euqal_json_value(expect_value[i], actual_value[i], key_path)
                    else:
                        self.__equal_field(sorted(actual_value),sorted(expect_value)[i], key_path)
            else:
                self.msg[key_path] = '实际结果与期望结果的长度不一致（注：list 比较必须相同）'
                self.assert_result.append(False)
                #
                # self._assert_error("JSON查询结果比较: 路径{0} 实际结果与期望结果的长度不一致（注：list 比较必须相同）！！".format(key_path))

    def __euqal_json_value(self, expect_value, actual_json, key_path=''):
        # json串的处理

        self.path_list = []  # 初始清空 路径 list
        if isinstance(expect_value, dict):  # 判断期望结果值是否为dict ，是进行 获取 key path操作 ,并且循环 key 获取value 进行校验。
            json_path_list = self.__get_json_path(expect_value)

            for i in json_path_list:
                expect_value_new = Tree(expect_value).execute("$."+i)
                actual_value_new = Tree(actual_json).execute("$."+i)
                if isinstance(expect_value_new, (list, tuple)) and expect_value_new and actual_value_new:  # 如果value 为list 调用 list 数据比较

                    if len(expect_value_new) == len(actual_value_new):

                        self.__euqal_list_value(expect_value_new, actual_value_new, key_path+'|'+i if key_path else key_path+i)

                    else:

                        self.msg[key_path+i] = '实际结果与期望结果的长度不一致（注：list 比较必须相同）'
                        self.assert_result.append(False)

                else:  # 否则直接调用数据比较
                    #更新key
                    key_path = i
                    self.__equal_field(expect_value_new, actual_value_new, key_path)

    def __euqal_path_value(self):
        # 此方法用于比较指定路径的值
        for k, v in self.__expect_json.items():
            expect_value = v
            actual_value = Tree(self.__actual_json).execute("$."+k)
            self.__equal_field(actual_value, expect_value, "$."+k)
    def __equal_field(self,expect_value, actual_value, path):
        # 结果比较
        if isinstance(actual_value, list) and isinstance(expect_value, list):
            if isinstance(expect_value, list) and len(set(actual_value) - set(expect_value)) != 0:
                self.msg[path] = '期望结果为：{1}, 实际结果值为：{2}'.format(actual_value, expect_value)
                self.assert_result.append(False)
                # self._assert_error(msg)


        elif isinstance(actual_value, list) and not isinstance(expect_value, list):
            if expect_value not in actual_value:
                self.msg[path] = '期望结果为：{1}, 实际结果值为：{2}'.format(actual_value, expect_value)
                self.assert_result.append(False)
                # self._assert_error(msg)

        else:
            if actual_value != expect_value:
                self.msg[path] = '期望结果为：{0}, 实际结果值为：{1}'.format(actual_value, expect_value)
                self.assert_result.append(False)
                # self._assert_error(msg)

    def _assert_error(self, msg):
        # 抛出异常
        raise AssertionError(msg)
    def assert_value(self, actual_json, expect_json):
        self.msg = {}
        self.assert_result = []
        self.__expect_json = self.__convert_json(expect_json)
        self.__actual_json = self.__convert_json(actual_json)
        keys_contain = [True for k in list(self.__expect_json.keys()) if '.' in k]   # 指定路径的path

        if len(keys_contain) == len(list(self.__expect_json.keys())):
            self.__euqal_path_value()
        else:
            self.__euqal_json_value(self.__expect_json, self.__actual_json)


        return self.assert_result, self.msg


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
        result_json_value = self.__convert_json(result)
        try:
            result_value = Tree(result_json_value).execute(path)
        except Exception as e:
            result_value = 'None'
            print(e)
        return result_value


# jv = JsonValue()
#
# aa = '{"respCode": "9987", "respMsg": "信息有误，请稍后操作", "data": null}'
# bb = '{"respCode": "1000","respMsg": "成功"}'
#
# print (jv.assert_value(aa, bb))

# json = {
#     "a":
#         {"a": "b",
#          "c": "d"
#         },
#     'a1':[[{'aa':1,"bb":1}],[{'aa1':1,"bb1":1}]],
#     "b": "c",
#     "content": {
#         "merchant": [
#             {
#                 "countInLine": [{'m':'m','n1':'n'}],
#                 "merchants": [],
#                 "hasLink": 0
#             },
#             {
#                 "countInLine": 12,
#                 "merchants": [],
#                 "hasLink": {"a": [{'e':2}]}
#             }
#         ],
#         "sequence": [
#             "banner",
#             "thumbnail",
#             "coupon",
#             "textArea",
#
#             "merchant",
#             "caption",
#             "product"
#         ],
#         "coupon": [
#             {
#                 "isShowCoupon": 1,
#                 "coupons": [
#                     {
#                         "merchantLogos": "https://sittest.memedai.cn:443/coupon/activity/getObject/{key:./url/merchant001.png}",
#                         "effectiveDatesEnd": "2020.07.30",
#                         "couponId": "9092555555550101",
#                         "discount": "3.0",
#                         "isGuanma": None,
#                         "amountLimits": "3000",
#                         "couponName": None,
#                         "amount": None,
#                         "effectiveDatesBegin": "2020.07.26",
#                         "type": 1,
#                         "periodLimits": None
#                     }
#                 ],
#                 "countInLine": 1
#             }
#         ]
# }
# }
#
#
# aa = {"content": {
#         "merchant": [
#             {
#                 "countInLine": [{'m':'m','n1':'n'}],
#                 "merchants": [],
#                 "hasLink": 0
#             },
#               {
#                 "countInLine": 12,
#                 "merchants": [],
#                  "hasLink": {"a": [{'e':2}]}
#             }
#         ],
#             "sequence": [
#             "banner",
#             "thumbnail",
#             "coupon",
#             "textArea",
#             "caption",
#             "merchant",
#             "product"
#         ]
# },
#       "a":
#         {"a": "b",
#          "c": "d"
#         },
#     "b": "c",
#     'a1':[[{'aa':1,"bb":1}],[{'aa1':1,"bb1":1}]],
# }
#
# bb = {"content.merchant[0].hasLink": 0,
#       "content.sequence": [
#             "banner",
#             "thumbnail",
#             "coupon",
#
#             "caption",
#             "merchant",
#             "textArea",
#             "product"
#         ]
#
# }
#
# at = {"qq": [{"countInLine": 12, "merchants": [], "hasLink": {"a": [{'e':2}]}}, {"countInLine": 12, "merchants": [{"a":1},{"b":[{"c":3},{"d":4}]}], "hasLink": {"a": [{'e':2}]}}]}
# bt = {"qq": [{"countInLine": 12, "merchants": [{"a":1},{"b":[{"c":3},{"d":4}]}], "hasLink": {"a": [{'e':2}]}}, {"countInLine": 12, "merchants": [], "hasLink": {"a": [{'e':2}]}}]}
# # print sorted(at["qq"])
# # print sorted(bt["qq"])
# jv.assert_value(at, bt)
# #存在BUG  list包含dict 并且数量不相等 是 比对出错
# # jv.assert_value(json, aa)
# # jv.assert_value(json, bb)

