#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import redis


class ExportFromMysql(object):
    def __init__(self):
        self.mysqlDB = None
        self.mysqlCursor = None
        self.redisDB = None
        self.subList = []

        # 连接DB
        self.connect_mysql()
        self.connect_redis()

    def process(self):
        """
        从Redis读取，写入Mysql 
        """
        self.query_subscribe_table()

        with open(r'C:\Users\youtian\Desktop\exp.mysql','w+') as f:
            for k in self.subList:
                f.write(k + "\n")


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

    def query_subscribe_table(self):
        """
        DB.取订阅表
        """
        sql = u"""
        SELECT mail, tel, sub_date FROM tmp_cot_subscribe_from_redis
        """
        self.mysqlCursor.execute(sql)
        for row in self.mysqlCursor.fetchall():
            self.subList.append(
                'subscribe_list:%s:%s:%s' %(row[2], row[1], row[0])
            )
            print(self.subList)

if __name__ == '__main__':
    export = ExportFromMysql()
    export.process()

