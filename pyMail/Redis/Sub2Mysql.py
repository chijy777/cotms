#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import redis


class Sub2Mysql(object):
    def __init__(self):
        self.mysqlDB = None
        self.mysqlCursor = None
        self.redisDB = None

        # 连接DB
        self.connect_mysql()
        self.connect_redis()


    def process(self):
        """
        从Redis读取，写入Mysql 
        """
        keys = self.redisDB.keys()
        print(len(keys), keys[0])

        with open(r'C:\Users\youtian\Desktop\exp.data','w+') as f:
            for k in keys:
                # l = k.split(':')
                # print(l)
                # self.insertSubTable(l[3], l[2], l[1])
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


    def insertSubTable(self, mail, tel, sub_date):
        """
        DB.插入订阅表.
        """
        sql = "INSERT INTO cot_subscribe_from_redis(mail, tel, sub_date, create_time, update_time) " \
              "VALUES('%s', '%s', '%s', UNIX_TIMESTAMP(now()), UNIX_TIMESTAMP(now()))" %(
                    mail, tel, sub_date
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
    sub = Sub2Mysql()
    sub.process()

