# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
import os, time, random
import re


# 写数据进程执行的代码
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
        print('Put %s to queue...' % value)
        q.put(value)
        sleep_time = 0.5#random.random()
        print('sleep %s' % sleep_time)
        time.sleep(sleep_time)


# 读取数据进程执行的代码
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue(pid: %s).' % (value, os.getpid()))


def queue_in_multi_process():
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pr2 = Process(target=read, args=(q,))
    pr3 = Process(target=read, args=(q,))
    # 启动子进程pw，写入：
    pw.start()
    # 启动子进程pr，读取：
    pr.start()
    pr2.start()
    pr3.start()
    # 等待pw结果：
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止：
    pr.terminate()
    pr2.terminate()
    pr3.terminate()


EMAIL_RE = re.compile(r'^[\w|_.]+@[\w]+\.[a-z]{3}$')
NAME_EMAIL_RE = re.compile(r'(?:<([a-zA-Z\s]+)>)?\s?([\w|_.]+)@([\w]+)\.([a-z]{3}$)')


def is_valid_email(addr):
    if EMAIL_RE.match(addr):
        print("%s is valid email address!" % addr)
        return True
    else:
        print("%s is not valid email address!" % addr)
        return False


def name_of_email(addr):
    m = NAME_EMAIL_RE.match(addr)
    if m:
        print("group[0]: %s " % m.group(0))
        print("group[1]: %s " % m.group(1))
        print("group[2]: %s " % m.group(2))
        print("group[3]: %s " % m.group(3))
        print("group[4]: %s " % m.group(4))
        if m.group(1):
            return m.group(1)
        else:
            return m.group(2)
    else:
        print("%s is not valid email address!" % addr)
        return None

'''
if __name__ == '__main__':
    # queue_in_multi_process()
    assert is_valid_email('someone@gmail.com')
    assert is_valid_email('bill.gates@microsoft.com')
    assert not is_valid_email('bob#example.com')
    assert not is_valid_email('mr-bob@example.com')
    print('ok')

    assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
    assert name_of_email('tom@voyager.org') == 'tom'
    print('ok')
'''