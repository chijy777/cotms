#!/usr/bin/python
#coding:utf-8
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://cot.io/PRE/subscribe.html")


# 表单填写.
driver.find_element_by_xpath(
    '//*[@id="doc-ipt-email-4"]'
).send_keys(
    "1178937142@qq.com"
)

driver.find_element_by_xpath(
    '//*[@id="doc-ipt-email-3"]'
).send_keys(
    "18910103433"
)

driver.find_element_by_xpath(
    '//*[@id="doc-ta-1"]'
).send_keys(
    "haha--"*21
)

driver.find_element_by_xpath(
    '//*[@id="inputCode"]'
).send_keys(
    "1234"
)

# 表单提交.
driver.find_element_by_xpath(
    '//*[@id="buttonClick"]'
).click()




# 关闭Firefox
# driver.close()
# driver.quit()

