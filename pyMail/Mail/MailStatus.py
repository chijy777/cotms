#!/usr/bin/python
#coding:utf-8
import requests
from Mail import settings


class MailStatus(object):

    def query(self):
        """
        查询.
        """
        url = 'http://api.sendcloud.net/apiv2/data/emailStatus'

        params = {
            "apiUser": settings.SEND_CLOUD_API_USER,
            "apiKey" : settings.SEND_CLOUD_API_KEY,
            "days"   : 2
        }
        # print(content)

        # 发送.
        result = requests.post(url, files={}, data=params)
        print(result.text)



if __name__ == '__main__':
    send = MailStatus()
    send.query()
