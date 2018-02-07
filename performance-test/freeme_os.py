#!/usr/bin/env python

import AppStartTime
import TestMode
from Logcat import Logout

version = '1.1'

if __name__ == "__main__":
    '''
        本程序用来统计应用启动时间，并求平均值
    '''
    Logout.show_message('\nStart...\n')
    TestMode.init()
    group = AppStartTime.GroupTest()
    group.preLoop()
    group.loopGroup()

    Logout.show_message('\n测试完成...')
