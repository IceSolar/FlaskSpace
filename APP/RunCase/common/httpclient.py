# -*- coding:utf-8 -*-
'''
requests 类的在封装，进行访问 http 请求
'''
__author__ = 'rundof han'
import requests
import json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()



class HttpClient:
    
    #初始化 
    def __init__(self):
        self._sobj = requests.Session()
        self.resp = None
        self.respon_json = {}
        self.respon_text = {}
    # 封装HTTP get请求方法
    def http_get(self, url, heard_info, param=None, time_data=30):
        # 调用方法 如果异常 resp 设置为NONE
        if param:
            if isinstance(param, str):
                self.param = json.loads(param)
            elif isinstance(param, (dict, json)):
                self.param = param
            else:
                self.param = eval(param)
        else:
            self.param = param

        if heard_info:
            if isinstance(heard_info, str):
                self.heard_info = json.loads(heard_info)
            elif isinstance(heard_info, (dict, json)):
                self.heard_info = heard_info
            else:
                self.heard_info = eval(heard_info)
        else:
            self.heard_info = heard_info


        try:
            self.resp = self._sobj.get(url, headers=self.heard_info, params=self.param, timeout=time_data)
        except Exception as e:
            print(e)
        return self.resp

    # 封装HTTP POST请求方法
    def http_post(self, url, heard_info, param=None, files=None, time_data=30):
        # 调用方法 如果异常 resp 设置为NONE
        if param:
            if isinstance(param, str) and '{' in param and '}' in param:
                self.param = param
            elif isinstance(param, dict):
                self.param = json.dumps(param)
            else:
                self.param = param.encode('utf-8')
        else:

            self.param = param

        if heard_info:
            if isinstance(heard_info, str):
                self.heard_info = eval(heard_info)
            elif isinstance(heard_info, (dict, json)):

                self.heard_info = heard_info
            else:

                self.heard_info = eval(heard_info)
        else:
            self.heard_info = heard_info
        try:
            self.resp = requests.post(url, headers=self.heard_info, data=self.param, files=files, verify=False, timeout=time_data)
        except Exception as e:
            print(e)
        else:
            return self.resp

    #r.status_code  allow_redirects = False r.headers  r.request.headers

    def get_json_data(self, pro):

        if pro:
            if pro.status_code == 200:
                try:
                    self.respon_json = pro.json()
                except:
                    self.respon_json = {'status_code': pro.status_code, 'desc': '未返回json数据'}
            else:
                self.respon_json = {'status_code': pro.status_code}
        else:
            self.respon_json = {'status_code': '11111', 'desc': '调用接口异常'}

        return self.respon_json

    def get_content_data(self, pro):

        if pro:
            if pro.status_code == 200:
                self.respon_text = pro.text
            else:
                self.respon_text = '自定义返回值 tatus_code： %s' % pro.status_code
        else:
            self.respon_text = '调用异常'

        return self.respon_text
#
# if __name__ == '__main__':
#     hc = HttpClient()
#
#     head_info ={"Content-Type": "application/x-www-form-urlencoded",
#                 "x-auth-token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJqd3QiLCJpYXQiOjE0OTM4OTAwMTUsInN1YiI6IntcInVzZXJOYW1lXCI6XCJhZG1pblwifSIsImV4cCI6MTQ5Mzg5MTgxNX0.IyoWrOIRJSnhMdlEc_PgIuTngvZG60RUEQ_cYO9unHg"
#                 }
#
#
#     params = "packageIds=bd0fa6ba-ae4b-4ba9-a4a4-0d9db8e31ff1&rateDate=2017-05-09"
#     #req = hc.http_post('    http://t.jufandev.com:8021/PAOP/asset/package/setStartTime', head_info, params)
#     req = hc.http_post('http://192.168.21.30:3000/PAOP/asset/package/setStartTime', head_info, params)
#
#     print(hc.get_json_data(req))