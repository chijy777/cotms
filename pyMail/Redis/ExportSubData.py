#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import pymysql
import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ExportSubData(object):
    def __init__(self):
        self.redisDB = None
        self.subList = []

        # 连接DB
        self.connect_redis()


    def process(self, str_date):
        """
        从Redis读取，写入文件 
        """
        fname = r'./exp_sub_%s.data' %(str_date)
        key = 'subscribe_list:%s' %(str_date)

        with open(fname,'a+') as f:
            for n in range(self.redisDB.llen(key)):
                # s = self.redisDB.lindex(key, n)
                # v = json.loads(s)
                # line = "%s | %s | %s | %s | %s | %s \n" %(
                #     v['emailAddress'], v['phoneNumber'], v['ipAddress'],
                #     v['date'], v['contentDetail'], v['validateFlag']
                # )
                # f.write(line)
                line = self.redisDB.lindex(key, n)
                f.write(line +'\n')

    def connect_redis(self):
        """
        连接REDIS
        """
        self.redisDB = redis.Redis(
            host='127.0.0.1',
            port=6666,
            db=1,
            password='cot2018'
        )

if __name__ == '__main__':
    export = ExportSubData()
    export.process('20180711')

