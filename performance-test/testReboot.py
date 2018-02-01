#!/usr/bin/env python
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md

a = 0
while a < 10000:
    device = mr.waitForConnection()
    device.wake()
    mr.sleep(3)
    device.reboot()
    print("test, {}".format(a))
    a = a + 1
    mr.sleep(30)
