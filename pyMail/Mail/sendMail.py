#!/usr/bin/python
#coding:utf-8
import json
import pymysql
import requests
from pyMail.Mail import settings


class SendMail(object):
    def __init__(self):
        self.mysqlDB = None
        self.mysqlCursor = None

        self.contentId = None
        self.subject = None
        self.body = None
        self.mailList = []

        # 连接DB
        self.connect_mysql()


    def send_mail(self):
        """
        发送邮件.
        """
        # 取邮件内容
        self.mysql_query_mail_content()

        # 取邮箱清单.
        self.mysql_query_waited_mail_list()

        # 测试号-测试.
        # self.mailList = ["1178937142@qq.com"]
        # self.mailList = ["2585747805@qq.com"]
        # self.mailList = [
        #     '2585747805@qq.com',
        #     '2317758329@qq.com',
        #     'jayeer@citiz.net',
        #     '17156309@qq.com',
        #     '1981211830@qq.com',
        #     '17156311@qq.com'
        # ]

        # 启动邮件发送，逐条发送.
        for mail in self.mailList:
            print(mail)
            self.send_one(mail, self.subject, self.body)

    def connect_mysql(self):
        """
        连接MYSQL 
        """
        self.mysqlDB = pymysql.Connect(
            host=settings.MYSQL['MYSQL_HOST'],
            user=settings.MYSQL['MYSQL_USER'],
            passwd=settings.MYSQL['MYSQL_PASSWD'],
            db=settings.MYSQL['MYSQL_DBNAME'],
            charset='utf8'
        )
        self.mysqlCursor = self.mysqlDB.cursor()

    
    def mysql_query_mail_content(self):
        """
        DB.取邮件内容.
        """
        sql = u"""
        SELECT id, subject, body FROM cot_mail_content WHERE state = 1
        """
        self.mysqlCursor.execute(sql)
        for row in self.mysqlCursor.fetchall():
            self.contentId = row[0]
            self.subject = row[1]
            self.body = row[2]
        print('%s | %s' %(self.subject, self.body))

    def mysql_query_waited_mail_list(self):
        """
        DB.取邮件地址列表.
        """
        self.mailList = []
        sql = u"""
        SELECT mail_id FROM cot_mail_send WHERE state = 0
        """
        self.mysqlCursor.execute(sql)
        for row in self.mysqlCursor.fetchall():
            self.mailList.append(row[0].strip())


    def mysql_update_mail_result(self, to_mail, result_txt):
        """
        DB.更新邮件发送结果.
        """
        json_result = json.loads(result_txt)
        print(json_result)

        #成功
        if(json_result['result'] == True):
            sql = "UPDATE cot_mail_send SET sender_name = '%s', sender_mail = '%s', send_result='%s', " \
                  "send_time=UNIX_TIMESTAMP(now()), state=1, update_time=UNIX_TIMESTAMP(now())" \
                  "WHERE mail_id='%s' AND content_id=%d" %(
                      settings.SEND_CLOUD_FROM_NAME, settings.SEND_CLOUD_FROM, result_txt, to_mail, self.contentId
                    )
        else:
            sql = "UPDATE cot_mail_send SET sender_name = '%s', sender_mail = '%s', send_result='%s', " \
                  "send_time=UNIX_TIMESTAMP(now()), state=-1 " \
                  "WHERE mail_id='%s' AND content_id=%d" % (
                      settings.SEND_CLOUD_FROM_NAME, settings.SEND_CLOUD_FROM, result_txt, to_mail, self.contentId
                    )
        # print(sql)
        try:
            self.mysqlCursor.execute(sql)
            self.mysqlDB.commit()
        except Exception as e:
            self.mysqlDB.rollback()
        # finally:
        #     self.mysqlDB.close()


    def send_one(self, to_mail, subject, body):
        """
        逐个文件发送.
        """
        content = {
            "apiUser": settings.SEND_CLOUD_API_USER,
            "apiKey" : settings.SEND_CLOUD_API_KEY,
            "from"   : settings.SEND_CLOUD_FROM,
            "fromName" : settings.SEND_CLOUD_FROM_NAME,
            "to": to_mail,
            "subject" : subject,
            "html": body,
        }
        # print(content)

        # 发送.
        result = requests.post(
            settings.SEND_CLOUD_API_URL, files={}, data=content
        )
        print(result.text)

        # 更新DB.
        self.mysql_update_mail_result(to_mail, result.text)


if __name__ == '__main__':
    send = SendMail()
    send.send_mail()
