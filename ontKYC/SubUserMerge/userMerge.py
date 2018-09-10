#!/usr/bin/python
#coding:utf-8
import json
import os
import pymysql
from SubUserInfoInit import config_user

class InitWx(object):
    """
    初始化，订阅者.微信信息.
    """
    def __init__(self):
        self.mysqlDB = None
        self.mysqlCursor = None

        self.dataList = []

        # 连接DB
        self.connect_mysql()

    def connect_mysql(self):
        """
        连接MYSQL
        """
        self.mysqlDB = pymysql.Connect(
            host= config_init.MYSQL['MYSQL_HOST'],
            user= config_init.MYSQL['MYSQL_USER'],
            passwd= config_init.MYSQL['MYSQL_PASSWD'],
            db= config_init.MYSQL['MYSQL_DBNAME'],
            charset='utf8',
            # charset ='utf8mb4',
        )
        self.mysqlCursor = self.mysqlDB.cursor()
        self.mysqlCursor.execute("SET NAMES utf8")


    def process(self):
        """
        初始化数据.
        1. 遍历目录.
        """
        dirPath = r'D:\COT\dev\_订阅_邮件\_（仲平）订阅数据\（仲平820）KYC认证数据\微信群8个'
        fileList = os.listdir(dirPath)   # 列出文件夹下所有的目录与文件

        # 遍历目录.
        for i in range(0, len(fileList)):
            path = os.path.join(dirPath, fileList[i])
            if not( os.path.isfile(path) ):
                continue

            filePath = os.path.abspath(path)
            # print("============>", filePath)
            if not (filePath.find('.json')>0):
                continue
            # 文件处理.
            self.process_single(filePath)
            # break


    def process_single(self, file_path):
        """
        处理每一个文件.
        """
        print("[process_single]============>", file_path)
        groupNo = file_path.split('交流群')[1].strip('.json')
        groupName = ('group%s')%(groupNo)
        print(groupName)

        if not (groupNo == '9'): # 测试.
            return

        with open(file_path, "r", encoding='UTF-8') as f:
            jsonData = json.loads(f.read())
            print("[{}][jsonData]====>{}/{}".format(groupName, len(jsonData), jsonData) )

            if jsonData and len(jsonData)>0:
                for one in jsonData:
                    # print('[{}][one]=====>city={}, country={}, head_img={}, nick_name={}, '
                    #       'province={}, remark_name={}, sex={}, user_name={}, wxid={}'.format(
                    #     groupName, one.get('city',None), one.get('country',None), one.get('head_img',None),
                    #     one.get('nick_name', None), one.get('province', None), one.get('remark_name', None),
                    #     one.get('sex', None), one.get('user_name', None), one.get('wxid', None)
                    # ))

                    # 插入，数据库.
                    ret = self.mysql_insert_sub_wx(
                        group_name=groupName, one_item=one
                    )
                    if not ret: # 入库异常.
                        if one.get('nick_name', None):
                            one['nick_name'] = ''
                        if one.get('city', None):
                            one['city'] = one['city'].replace('\'', '')
                        ret = self.mysql_insert_sub_wx(
                            group_name=groupName, one_item=one
                        )


    def mysql_insert_sub_wx(self, group_name, one_item):
        """
        DB.插入[cot_sub_wx_info]表.
        """
        if self.mysql_is_exist_sub_wx(one_item.get('wxid',None)) > 0:
            return

        print("[not_exist]=====>wx_id={} is not exists.".format(one_item.get('wxid', None)))

        sql = "INSERT INTO cot_sub_wx_info(wxid, user_name, nick_name, remark_name, sex, " \
              " head_img, city, province, country, from_group," \
              " create_time, update_time) " \
              " VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()))"  % (
                    one_item.get('wxid', ''), one_item.get('user_name', ''), one_item.get('nick_name', ''),
                    one_item.get('remark_name', ''), one_item.get('sex', ''), one_item.get('head_img', ''),
                    one_item.get('city', ''), one_item.get('province', ''), one_item.get('country', ''),
                    group_name,
              )
        print("[sql]=====>", sql)

        try:
            self.mysqlCursor.execute(sql)
            self.mysqlDB.commit()
            return 1
        except Exception as e:
            print('######################', e)
            self.mysqlDB.rollback()
            return 0
        # finally:
        #     self.mysqlDB.close()


    def mysql_is_exist_sub_wx(self, wx_id):
        """
        DB.取邮件内容.
        """
        if not wx_id:
            return None

        sql = u"SELECT count(*) FROM cot_sub_wx_info WHERE wxid = '%s' " %(wx_id)

        self.mysqlCursor.execute(sql)
        for row in self.mysqlCursor.fetchall():
            if int(row[0]) > 0:
                print("aaa==========>{} | {}".format(wx_id, int(row[0])))
                return int(row[0])


if __name__ == '__main__':
    wx = InitWx()
    wx.process()
