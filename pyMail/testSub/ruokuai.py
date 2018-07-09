#!/usr/bin/env python
# coding:utf-8
import requests
from hashlib import md5

class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key

        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {
            'image': ('a.jpg', im)
        }
        r = requests.post(
            'http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers
        )
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post(
            'http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers
        )
        return r.json()


if __name__ == '__main__':
    rc = RClient(
        username = u'chijy777',
        password = 'chijy123'.encode('utf-8'),
        soft_id = '107665',
        soft_key = '66ea7b2c550445b8bd97a70bd0af85b0'
    )
    im = open(
        r'C:\Users\youtian\Desktop\a.png', 'rb'
    ).read()
    print(
        rc.rk_create(im, 3040)
    )

