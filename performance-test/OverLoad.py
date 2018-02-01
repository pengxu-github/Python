#!/usr/bin/env python

import os
import sys
import time
from Logcat import Logout
from CommandExecuter import CommandExecuter
from TestMode import getOverloadPaths

DEBUG = False


class OverLoad:

    def __init__(self):
        self.overload_path = 0
        self.paths = getOverloadPaths()

    def choose_overload_path(self):
        paths = self.getPaths();
        while True:
            for path in paths:
                Logout.show_message(path)
            index = input("\n请选择重载路径：")
            itemIndex = 0

            if self.checkInput(index) == 0:
                itemIndex = int(index)
            else:
                Logout.show_message('输入无效，请重新输入！！！')
                continue

            if itemIndex <= 0 or itemIndex > len(paths):
                Logout.show_message('输入无效，请重新输入！！！')
                continue
            self.overload_path = itemIndex
            return index

        return 0

    def checkInput(self, index):
        if index.isdigit():
            return 0
        else:
            return -1

    def getPaths(self):
        selections = []

        for i in range(len(self.paths)):
            path = self.paths[i]
            message = str(i + 1) + ' : '
            for j in range(len(path)):
                item = path[j]
                message += item[0]
                if j < len(path) - 1:
                    message += '->'
            selections.append(message)

        return selections

    def getOverLoadPath(self):
        return self.paths[self.overload_path - 1]

    def executeOverload(self):
        for item in self.paths[self.overload_path - 1]:
            CommandExecuter.execute_command('adb shell am start -W ' + item[1])
            time.sleep(1)
            CommandExecuter.pressHome()


if __name__ == "__main__":
    Logout.show_message('Please pre-call me if you want to start apps in Overload Mode!!!')
# paths = OverLoad()
# paths.choose_overload_path()
# paths.executeOverload()
