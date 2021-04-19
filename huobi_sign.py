# -*- encoding: utf-8 -*-
'''
@File    :   sgin.py
@Time    :   2021/03/10 20:22:16
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
import requests
import base64
import hashlib
import urllib
import datetime
import hmac

accesskey = "XXXXX"
secretkey = "YYYYY"

class SIGN(object):
    def __init__(self, accesskey: str, secretkey: str):
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.url = "api.huobi.pro"
    
    def sign(self, to_url: str):
        param_data = {
            "AccessKeyId": self.accesskey,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": 2,
            "Timestamp": urllib.parse.quote(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
        }
        self.sorted_url = "&".join([i + "=" + str(param_data[i]) for i in sorted(param_data.keys())])
        sign_str = "GET\n" + self.url + "\n" + to_url + "\n" + self.sorted_url
        key = self.secretkey.encode('utf-8')
        message = sign_str.encode('utf-8')
        sign = base64.b64encode(
            hmac.new(key, message, digestmod=hashlib.sha256).digest())
        sign = str(sign, 'utf-8')
        return sign

    def accounts(self):
        to_url = "/v1/account/accounts"
        siginature = self.sign(to_url)
        url = "https://" + self.url + to_url + "?" +self.sorted_url + "&Signature=" + siginature
        get_data = requests.get(url)
        if get_data.status_code == 200:
            return get_data.json()
        else:
            return "error"


sign = SIGN(accesskey, secretkey)

print(sign.accounts())
