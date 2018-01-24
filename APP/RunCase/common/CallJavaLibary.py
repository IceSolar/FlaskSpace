# -*- coding:utf-8 -*-
'''
Created on 2016-8-19
 
@author: Rudolf Han
'''

import jpype
import time
import random
import urllib.parse

#def __startJVM():
#    
#    #获取当前路径 下的 ，并且获取到 jars 路径，作为加载
#    jarpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jars'))
#    jarpath = jarpath.replace('\\', '/')
#    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)  


class CallJavaLibary(object):

    def __init__(self):
#        jarpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jars'))
#        jarpath = jarpath.replace('\\', '/')
#    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)  
        #获取到都被dubbo 写的公共类
        #固定路径 调试路径 
        jarpath="C:\\jars"
        #生产路径 ： C:\AUTOTEST\workspace\AutoTestCase\PublicLibary\jars
#        jpype.shutdownJVM()
        if jpype.isJVMStarted():
            jpype.shutdownJVM()
            jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)
        else:
            jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)

    def __shutdownJVM(self):
        jpype.shutdownJVM()
    
    def Encrypt_RAS_Key(self, privateKeyStr, data):
        # 参数数据
        try:
            RSAKeyPairUtil=jpype.JClass("com.raskey.RSAKeyPairUtil")
            ras_key =RSAKeyPairUtil()
            result = ras_key.encryptRSA(privateKeyStr, data)
        except Exception as e:

            print('调用jar 包异常')
            print(e)
            result = None
        return result
        # return self.result



# data_json = {"applyAmt": "5000",
#  "backUrl": "http://t.94ym.cn/#/order/fqlist",
#  "hosCode": "10021",
#  "notifyUrl": "http://api.94ym.cn/pay/notify",
#  "orderNo": "100051",
#  "outUserId": "15",
#  "platform": "yaomei",
#  "projCode": "1",
#  "projName": "测试",
#  "randomNum":  str(int(round(time.time() * 1000)))+str(random.randint(1000, 9999))}


data_json = {"applyAmt":"2000",
 "backUrl":"http://t.94ym.cn/#/order/fqlist",
 "hosCode":"10021",
 "notifyUrl":"http://api.94ym.cn/pay/notify",
 "orderNo":"100058",
 "outUserId":"15",
 "platform":"yaomei",
 "projCode":"1",
 "projName":"测试",
 "randomNum":"14967441950958673"
}


keys = data_json.keys()
# print(keys)
list(keys).sort()
url_encode = urllib.parse.urlencode(data_json)


privateKeyStr = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBANXg0cYo1gGG0OMo9bGShYB5wNukLSoZEsZ77y0YS9GayFjSrPshABdapLOpquWi3ITLWARqnQhiCPFEzS3OI4GtZH2MUd4UK8q/NcDOI3afFBq3GZX1ZwzvwTbZfynCnIaNHgvwpjFdKzooWoS3vybcMXlF6B4SksPPNWGX6pWrAgMBAAECgYAWH4IzaCfy0noq9SKs8oYCqxVq4smVMDDD/S/ZT0kQbl1I6snf1CMJR2P//Y3i4PzEc7AwDMMfidx48G/0y/zaDaaeT51DJ8CWqIbUfZMDQE2I00g3tTyDZW/r0VQhYMOREi5ky+yZnVvfsihrcP1e493Ock06D4n4Zx6ORZAMWQJBAO13MwT2WUk/VN4K5Pt4USccYsjIPAYXNbcoKYa7M9N9bZQ0TLK5r1jNUwef6ESh8/tcabQM5Z/bof8SNYYiENcCQQDmklHiRVKHVhuVDh6v6C3XGjrJ/Mx+IDJibZOQUn3s0eoxUIC7IhypL9Q+q9KpsI6ikkhmZxVf3r+WGJ8OLwNNAkEA3Eeowj+rz7C6D0fX5hZUYY2JbWuhkpzRLVhKPTtG9jbyAXsKcvig2iWNkhMaKSB67X9qZqVYFRRuj+jaUdUj/QJBAJTbrH/f74sufXo69nbs+ANijMfxLPjUwpKnWdiYWXI2h/M0nRezyzszhNy9Q7GIKl4tAQ8TyEnv3lMCLFYU5hUCQGVFYFDmF3B5sqkG7Pi9gftDNw7qs3o1IgwpLoqq05Ai9rGew1bK/Mi0VMMQLjWW01zZYb/Kf4zino3geHvzn+k=";
#pwd = "applyAmt=5000&backUrl=http%3A%2F%2Ft.94ym.cn%2F%23%2Forder%2Ffqlist&hosCode=10021&notifyUrl=http%3A%2F%2Fapi.94ym.cn%2Fpay%2Fnotify&orderNo=100051&outUserId=15&platform=yaomei&projCode=1&projName=%E6%B5%8B%E8%AF%95&randomNum=14967374673984229";
dub = CallJavaLibary()
singn = dub.Encrypt_RAS_Key(privateKeyStr, url_encode)
# aa = urllib.parse.quote(singn)
print(urllib.parse.quote(singn))
url_encode_new = url_encode+"&sign="+urllib.parse.quote(singn)
request_list = []
for i in url_encode_new.split('&'):
    request_list.append(i.split("="))
json_new = dict(request_list)
print (json_new)