#!/usr/bin/python
#coding:utf-8
import threading
from Test.SubTest import SubTest


proclist=[]

def run(param):
    st = SubTest(param)
    lastVerifyCode = ''
    for i in range(1):
        print("thread_no=[%d], deal_no=[%d]=================" % (param, i))
        verifyCode = st.process()
        if (verifyCode != lastVerifyCode):  # 打码ok.
            lastVerifyCode = verifyCode
        else:  # 打码fail.
            st.start()
    st.close()

# def run(param):
#     for i in range(2):
#         print("I was listening to %s-%s. %s" %(param, i, time.time()))
#         time.sleep(1)


for i in range(10):
    proc = threading.Thread(target=run, args=(i,) )
    proclist.append(proc)

for proc in proclist:
    proc.start()

for proc in proclist:
    proc.join()
