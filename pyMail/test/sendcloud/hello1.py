#!/usr/bin/python
#coding:utf-8
import requests, json

"""
发信域名	KVYvxImAmEBlfUaNqidmyXw7zvijepgx.sendcloud.org
API_USER	chijy777_test_TbNuhy
API_KEY	这里是您手动生成的API_KEY
"""

url="http://api.sendcloud.net/apiv2/mail/send"

# 您需要登录SendCloud创建API_USER，使用API_USER和API_KEY才可以进行邮件的发送。
params = {
    "apiUser": "chijy777_test_TbNuhy",
    "apiKey" : "2v6yRT9hrHO6PERD",
    "from" : "service@sendcloud.im",
    "fromName" : "SendCloud测试邮件",
    "to" : "1178937142@qq.com",
    "subject" : "来自SendCloud的第一封邮件！",
    "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！",
}

r = requests.post(url, files={}, data=params)
print(r.text)
