#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import pymysql


class ImportSubData(object):
    def __init__(self):
        self.redisDB = None
        self.subList = []

        # 连接DB
        self.connect_mysql()


    def connect_mysql(self):
        """
        连接MYSQL 
        """
        self.mysqlDB = pymysql.Connect(
            host='123.56.201.94',
            user='root',
            passwd='youtiandai0)',
            db='cotms',
            charset='utf8'
        )
        self.mysqlCursor = self.mysqlDB.cursor()


    def process(self, fname):
        """
        读文件，写入Mysql
        """
        with open(fname,'rb') as f:
            for n, line in enumerate(f.readlines()):
                print("%s-->%s" %(n, line))
                v = json.loads(line)
                if n < 117400:
                    continue
                # s = "%s | %s | %s | %s | %s | %s \n" %(
                #     v['emailAddress'], v['phoneNumber'], v['ipAddress'], v['date'], v['contentDetail'], v['validateFlag']
                # )
                # print(s)

                #插入数据库
                self.insertSubTable(v)


    def insertSubTable(self, row):
        """
        DB.插入订阅表.
        """
        sql = "INSERT INTO tmp_sub_origin_713(mail, tel, ip, content, subtime, flag) " \
              "VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(
                    row['emailAddress'], row['phoneNumber'], row['ipAddress'], row['contentDetail'], row['date'], row['validateFlag']
               )
        # print(sql)
        try:
            self.mysqlCursor.execute(sql)
            self.mysqlDB.commit()
        except Exception as e:
            self.mysqlDB.rollback()
        # finally:
        #     self.mysqlDB.close()


if __name__ == '__main__':
    imp = ImportSubData()
    # imp.process('./exp_sub_20180711.data')
    imp.process('./exp_sub_20180713.data')
