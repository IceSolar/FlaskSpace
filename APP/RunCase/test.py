# import base64
# import hashlib
# import rsa
# from Crypto.PublicKey import RSA
#
# signKeyModHex  = "cc8e3eb61179e5257ea3adaa3329a49f1ac1776f8d52081c01208b1e70c8251e919e217cc31da5f4faee2b87fa4129b9f26a8127c565345b8a078356d59d3594202afc9e97a131a8d9a94196f0f8b397d5ff1c98b2a2a12fca8696409259507cf841193bed7e69469909b1061a0bd2fb42ae43beef8600b1312a2e36d9127f95"
# signKeyExpHex  = "ed7673f6887329404db35577afcd37fe3be13bf593e916e0ebae0bd25abafddc6ecf53b0b21149070c06512299b1ebeea12c62a2f8d473e39069085f55bc1ae4b69058ddee5d96e4ee5fd90a9f42b7b8fc4e6b096d08a55a8e643091294bd680e5d2dd8ff599f17a2883ccf63fe69b474467c539de6709609c9bc4cd36c8121"
#
# n = int(signKeyModHex,16)
# d = int(signKeyExpHex,16)
# sign_str = "123456"
#
# # 方法一:
# # 说明:
# # rsa.key.PrivateKey原型: def __init__(self, n, e, d, p, q, exp1=None, exp2=None, coef=None):
# # 当coef参数为空时, p、q不能为0; coef参数为1时, p、q可为0。因为仅仅只有n、d参数已知。
# privatekey = rsa.key.PrivateKey(n,0,d,0,0,coef=1)
#
# # 方法二：
# impl = RSA.RSAImplementation(use_fast_math=False)
# privatekey = impl.construct((n, 0))
# privatekey.key.d = d
#
# # 方法三(使用PKCS#1格式导入)：
# with open('rsa_private_key.pem', 'rb') as privatefile:
#     keydata = privatefile.read()
# privatekey = rsa.PrivateKey.load_pkcs1(keydata)
#
#
# # 对字符串加密签名
# signature = rsa.sign(sign_str.encode('utf-8'), privatekey, 'SHA-1')
# signature_base64 = base64.b64encode(signature).decode('utf-8')
#
# print(signature)
# print(signature_base64)

import urllib.parse
import time
import random
# outUserId=2&platform=yaomei&projName=牙齿种植&projCode=1&randomNum=14966469402526

data = {
'applyAmt': 2000,
'backUrl': 'http://t.94ym.cn/#/order/fqlist',
'hosCode': 10021,
'notifyUrl': 'http://Fapi.94ym.cn/Fpay/Fnotify',
'orderNo': str((time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))),
'outUserId': 2,
'platform': 'yaomei',
'projName': '牙齿种植',
'projCode': 1,
'randomNum': str(int(time.time())) + '000' + str(random.randint(1000, 9999)),
}

data_json = {"applyAmt": "5000",
 "backUrl": "http://t.94ym.cn/#/order/fqlist",
 "hosCode": "10021",
 "notifyUrl": "http://api.94ym.cn/pay/notify",
 "orderNo": "100051",
 "outUserId": "15",
 "platform": "yaomei",
 "projCode": "1",
 "projName": "测试",
 "randomNum":  str(int(round(time.time() * 1000)))+str(random.randint(1000, 9999))}



date1 = {
'sign': 'RTJCB24NGRGI4m5Q7wvRmnhGwHzJoZq5rnLEdNkoKNl682+AqXyFrKzMRmUXoLUObt2fN72/VRJoTHU9P2pN4oRJx6lA6GD35/Jdp+CDq0vL5x+IsqrKU92eMxQN3EXWysuxPKLzIOBqrcaEFnJo+qP67gTlmJYrZk0C7kpZWjs='
}
keys = data_json.keys()
# print(keys)
list(keys).sort()
print(map(data_json.get, keys))
url_encode = urllib.parse.urlencode(data_json)
print(url_encode)



keys = date1.keys()
# print(keys)
list(keys).sort()
print(map(date1.get, keys))
print(urllib.parse.urlencode(date1))