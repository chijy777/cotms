# -*- coding: utf-8 -*-
from string import Template

from Mail.sendMailBase import SendMailBase


class SendMailTmplOntid(SendMailBase):
    """
    邮件发送，带Ontid参数.
    """
    def send_mail(self):
        """
        发送邮件，处理.
        """
        # 取，邮箱清单.
        self.mysql_query_waited_mail_list()

        # 测试号-测试.
        self.mailList = [
            "1178937142@qq.com"  # 迟金岩.
            # self.mailList = "2585747805@qq.com",  # 仲平.
        ]


        # 取，邮件内容.
        self.mysql_query_mail_content()

        # 启动邮件发送，逐条发送.
        if self.mailList and len(self.mailList) > 0 and self.subject and self.body:
            for mail in self.mailList:
                print("mail={}".format(mail))

                # 更新邮件内容，替换ontid变量.
                newBody = self.update_param_ontid(
                    mail=mail, old_body=self.body+"<p>ontid============>${ontid}</p>"
                )

                # 发送，单条邮件.
                # self.send_one(
                #     to_mail=mail, subject=self.subject, body=newBody
                # )


    def update_param_ontid(self, mail, old_body):
        """
        更新邮件内容，替换ontid变量.
        """
        sql = u"""
            SELECT user_ontid FROM kyc910_res WHERE email = '{}'
        """.format(mail)

        self.mysqlCursor.execute(sql)

        row = self.mysqlCursor.fetchone()
        if row and row[0].strip():
            ontId = row[0].strip()
            print("===========>",ontId)

            tmpl = Template(old_body)
            newBody = tmpl.substitute(ontid=ontId)
            print("===========>", newBody)
            return newBody



if __name__ == '__main__':
    send = SendMailTmplOntid()
    send.send_mail()
