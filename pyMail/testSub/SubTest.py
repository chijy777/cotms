#!/usr/bin/python
#coding:utf-8
import datetime,time
from lxml import etree
from PIL import Image
from selenium import webdriver
from testSub.ruokuai import RClient


class SubTest(object):
    def __init__(self, sn):
        self.mail = "1178937142@qq.com"
        self.phone = "18910103433"
        self.content = "haha--"*21

        self.sn = sn #序列号.

        self.RK = RClient(
            username=u'chijy777',
            password='chijy123'.encode('utf-8'),
            soft_id='107665',
            soft_key='66ea7b2c550445b8bd97a70bd0af85b0'
        )

        # 启动
        self.start()


    def start(self):
        """
        启动FireFox
        """
        self.driver = webdriver.Firefox()
        self.driver.get("https://cot.io/PRE/subscribe.html")

    def process(self):
        """
        表单填写&提交
        """
        # 邮箱 - 表单填写.
        self.driver.find_element_by_xpath('//*[@id="doc-ipt-email-4"]').send_keys(self.mail)
        # print(self.driver.find_element_by_xpath('//*[@id="doc-ipt-email-4"]').text)

        # 手机号 - 表单填写.
        self.driver.find_element_by_xpath('//*[@id="doc-ipt-email-3"]').send_keys(self.phone)

        # 理解&建议 - 表单填写.
        self.driver.find_element_by_xpath('//*[@id="doc-ta-1"]').send_keys(self.content)

        #校验码 - 表单填写.
        # vc = ''
        vc = self.auto_setVerifyCode(
            screenShot_img = r'C:\Users\youtian\Desktop\ss%d.png' %(self.sn),
            verifyCode_img = r'C:\Users\youtian\Desktop\vc%d.png' %(self.sn)
        )

        # 开始计时.
        startTm = datetime.datetime.now()

        # 点击 - 提交button.
        self.driver.find_element_by_xpath('//*[@id="buttonClick"]').click()

        # 是否刷新.
        # htmlbody = self.driver.page_source.encode('utf-8')
        # selector = etree.HTML(htmlbody)
        # results = selector.xpath('//*[@id="doc-ipt-email-4"]/text()')
        # for result in results:
        #     print('==============|'+ result.xpath('string(.)').strip())
        # # mailTxt = links[0]
        # idTxt = self.driver.find_element_by_id('buttonClick').text
        # print(idTxt)
        # idAttr = self.driver.find_element_by_id('buttonClick').get_attribute("onclick")
        # print(idAttr)

        # 计算时间差.(毫秒)
        endTm = datetime.datetime.now()
        diffTm = (endTm - startTm).total_seconds()
        print( "cost_time=%d" %int(round(diffTm * 1000)) )

        # 最大等待时间.
        time.sleep(10)
        # self.driver.implicitly_wait(10)

        return vc


    def auto_setVerifyCode(self, screenShot_img, verifyCode_img):
        """
        自动设置验证码
        """
        self.driver.save_screenshot(screenShot_img)
        imgelement = self.driver.find_element_by_xpath('//*[@id="imageId"]')  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (
            int(location['x']), int(location['y']), int(location['x'] + size['width']),
            int(location['y'] + size['height'])
        )
        # 写成我们需要截取的位置坐标
        i = Image.open(screenShot_img)  # 打开截图
        frame = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame.save(verifyCode_img)

        rkIM = open(verifyCode_img, 'rb').read()
        rkJson = self.RK.rk_create(im=rkIM, im_type=3040)
        print(rkJson)
        if rkJson:
            verifyCode = rkJson['Result']
            self.driver.find_element_by_xpath('//*[@id="inputCode"]').send_keys(verifyCode)
            return verifyCode


    def close(self):
        """
        关闭Firefox
        """
        self.driver.close()
        # self.driver.quit()


if __name__ == '__main__':
    st = SubTest(0)

    lastVerifyCode = ''
    for i in range(10):
        print( "[%d]================="%(i) )
        verifyCode = st.process()

        if(verifyCode != lastVerifyCode): # 打码ok.
            lastVerifyCode = verifyCode
        else: # 打码fail.
            # st.close()
            st.start()
