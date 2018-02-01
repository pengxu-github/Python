#!/usr/bin/env python

from Logcat import *
from CommandExecuter import *

APPS_LIST = ['com.tencent.mm', 'com.tencent.mobileqq']


def ps_exists(name):
    (status, output) = CommandExecuter.execute_command('adb shell ps')
    if status == 0:
        ps_list = ''.join(output)
        if ps_list.find(name) != -1:
            return (0, output)
        else:
            return (-1, output)

    return (-1, output)


def tencent_mm_exists():
    (status, output) = ps_exists(APPS_LIST[0])
    if status == 0:
        return 0
    else:
        return -1


def tencent_qq_exists():
    (status, output) = ps_exists(APPS_LIST[1])
    if status == 0:
        return 0
    else:
        return -1


if __name__ == "__main__":
    Logout.show_message('I can print ps info')
# result = tencent_mm_exists()
# Logout.show_message('qq : ' + str(result))
