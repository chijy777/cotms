#!/usr/bin/python
#coding:utf-8
import threading

import time

proclist=[]
s=0

def music(func):
    for i in range(2):
        print("I was listening to %s-%d. %s" %(func, i, time.time()))
        time.sleep(1)


for i in range(2):
    proc = threading.Thread(target=music, args=(i,) )
    proclist.append(proc)

for proc in proclist:
    proc.start()

for proc in proclist:
    proc.join()
