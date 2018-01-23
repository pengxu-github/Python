# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        sleep_time = random.random()
        print('sleep %s' % sleep_time)
        time.sleep(sleep_time)

#读取数据进程执行的代码
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue(pid: %s).' % (value, os.getpid()))

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pr2 = Process(target=read, args=(q,))
    # 启动子进程pw，写入：
    pw.start()
    # 启动子进程pr，读取：
    pr.start()
    pr2.start()
    # 等待pw结果：
    pw.join()
    #pr进程里是死循环，无法等待其结束，只能强行终止：
    pr.terminate()
    pr2.terminate()
