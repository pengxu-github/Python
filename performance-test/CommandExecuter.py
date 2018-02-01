#!/usr/bin/env python

import subprocess
from Logcat import *


class CommandExecuter:
    '''CommandExecuter'''

    @staticmethod
    def execute_command(command):
        (status, ouput) = subprocess.getstatusoutput(command)
        return status, ouput

    @staticmethod
    def doubleBack():
        CommandExecuter.execute_command('adb shell input keyevent 4')
        CommandExecuter.execute_command('adb shell input keyevent 4')

    @staticmethod
    def pressHome():
        CommandExecuter.execute_command('adb shell input keyevent 3')


if __name__ == "__main__":
    Logout.show_message('I am CommandExecuter!!!')
