# -*- coding: utf-8 -*-
from Mail.sendMailBase import SendMailBase


class SendMail(SendMailBase):
    """
    """
    def send_mail(self):
        """
        发送邮件处理.
        """
        # 取，邮件内容.
        self.mysql_query_mail_content()

        # 取，邮箱清单.
        self.mysql_query_waited_mail_list()

        # 测试，测试号.
        self.mailList = [
            "1178937142@qq.com",  # 迟金岩.
            # "2585747805@qq.com",  # 仲平.

            # '2317758329@qq.com',
            # 'jayeer@citiz.net',
            # '17156309@qq.com',
            # '1981211830@qq.com',
            # '17156311@qq.com'
        ]

        # 启动邮件发送，逐条发送.
        for mail in self.mailList:
            print(mail)
            self.send_one(mail, self.subject, self.body)


if __name__ == '__main__':
    send = SendMail()
    send.send_mail()
