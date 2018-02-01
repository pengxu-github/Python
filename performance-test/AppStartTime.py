#!/usr/bin/env python

import os
import sys
import subprocess
import time
import xlwt
from CommandExecuter import CommandExecuter
from OverLoad import OverLoad
from Logcat import Logout
import PsUtils
import TestMode
from TestItem import TestItem
from Parser import Parser

DEBUG = True


class UserInput:
    def __init__(self):
        self.test_count = 0
        self.overload_path = 0
        self.all_apps = TestMode.getAllAppsList()

    def input(self):
        apps_item = self.choose_candidate()

        Logout.show_message('\n您选择了:\n ')

        for i in range(len(apps_item)):
            Logout.show_message(self.all_apps[int(apps_item[i])][0])

        Logout.show_message("\n正在清理临时文件...")

        for i in range(len(apps_item)):
            clearn_result = Logout.clearn_logout(self.all_apps[int(apps_item[i])])
            if clearn_result != 0:
                Logout.show_message("！！！删除文件失败，重试！！！")
                os._exit(0)

        Logout.show_message("\n临时文件清理完毕！\n")

        self.test_count = self.get_input_count()
        return apps_item, self.test_count

    def get_input_count(self):
        test_time = 0
        while True:
            count = input("请输入测试次数(>=4): ")
            if count.isdigit():
                test_time = int(count)
                if test_time <= 3:
                    Logout.show_message('测试次数需大于三次 \n')
                    continue
                else:
                    break
            else:
                test_time = 0
                Logout.show_message('ERROR! 请重新输入 \n')

        return test_time

    def checkInput(self, index):
        if index.isdigit():
            itemIndex = int(index)
            if itemIndex < 0 or itemIndex >= len(self.all_apps):
                return -1
        else:
            return -1
        return 0

    def choose_candidate(self):
        ITEM = ['', '', '']
        while True:
            checked = True
            for i in range(len(self.all_apps)):
                item = self.all_apps[i]
                Logout.show_message(str(i) + '	' + item[0])

            id_Str = input('\n请选择需要测试的应用代号(多个使用空格隔开)：')
            id_Str = id_Str.strip()
            ITEM = selected_list = id_Str.split(' ')

            Logout.show_message(selected_list)

            for i in range(len(selected_list)):
                item = selected_list[i]
                if self.checkInput(item) == -1:
                    Logout.show_message('！！！输入无效，请重新输入！！！')
                    checked = False
                    break

            if checked:
                return ITEM
        return ITEM


class ItemTest:
    def __init__(self, app_item, testTime, paths, overload):
        Logout.show_message('ItemTest init')
        self.app_item = app_item
        self.testTime = testTime
        self.paths = paths
        self.overload = overload
        self.current_loop_times = 0
        self.test_times_avaliable = 0
        self.tencent_mm_killed = 0
        self.tencent_qq_killed = 0

        self.wb = xlwt.Workbook()
        self.style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
        self.ws = self.wb.add_sheet('Start Activity Time')

        self.THISTIMEAVERAGE = 0
        self.TOTALTIMEAVERAGE = 0
        self.WAITTIMEAVERAGE = 0

        # [thisTime, totalTime, waitTime]
        self.MAX_ITEM = [0, 0, 0]
        self.MIN_ITEM = [100000000, 100000000, 100000000]

    def write_to_excel(self, ws, columes, thisTime, totalTime, waitTime):
        '''write_to_excel
            将测试结果缓存到 excel 表格中
        '''
        if DEBUG:
            Logout.show_message("write_to_excel")
        ws.write(columes, 0, "ThisTime")
        ws.write(columes, 1, int(thisTime))
        ws.write(columes, 2, "TotalTime")
        ws.write(columes, 3, int(totalTime))
        ws.write(columes, 4, "WaitTime")
        ws.write(columes, 5, int(waitTime))

    def start(self):
        Logout.show_message('Testing...' + self.app_item[0])

        while (self.current_loop_times < self.testTime):
            if self.overload:
                self.paths.executeOverload()
            result = self.__loopOnce()
            Logout.show_message("计次： " + str(self.current_loop_times + 1))
            if result == 1:
                self.test_times_avaliable += 1
                Logout.show_message("有效记录： " + str(self.test_times_avaliable))
            self.current_loop_times += 1
            time.sleep(1)

        Logout.show_message("\n预设测试次数： " + str(self.testTime))
        Logout.show_message("有效测试次数： " + str(self.test_times_avaliable))

        Logout.show_message("\nthisTime max, min: " + str(self.MAX_ITEM[0]) + ", " + str(self.MIN_ITEM[0]))
        Logout.show_message("totalTime max, min: " + str(self.MAX_ITEM[1]) + ", " + str(self.MIN_ITEM[1]))
        Logout.show_message("waitTime max, min: " + str(self.MAX_ITEM[2]) + ", " + str(self.MIN_ITEM[2]))

        Logout.show_message("\nsum thisTime: " + str(self.THISTIMEAVERAGE))
        Logout.show_message("\nsum totalTime: " + str(self.TOTALTIMEAVERAGE))
        Logout.show_message("\nsum waitTime: " + str(self.WAITTIMEAVERAGE))

        if self.test_times_avaliable >= 3:
            THISTIMEAVERAGE = (self.THISTIMEAVERAGE - self.MAX_ITEM[0] - self.MIN_ITEM[0]) / (
                        self.test_times_avaliable - 2)
            TOTALTIMEAVERAGE = (self.TOTALTIMEAVERAGE - self.MAX_ITEM[1] - self.MIN_ITEM[1]) / (
                        self.test_times_avaliable - 2)
            WAITTIMEAVERAGE = (self.WAITTIMEAVERAGE - self.MAX_ITEM[2] - self.MIN_ITEM[2]) / (
                        self.test_times_avaliable - 2)
            self.ws.write(self.test_times_avaliable, 1, THISTIMEAVERAGE, self.style0)
            self.ws.write(self.test_times_avaliable, 3, TOTALTIMEAVERAGE, self.style0)
            self.ws.write(self.test_times_avaliable, 5, WAITTIMEAVERAGE, self.style0)
        elif self.test_times_avaliable > 0:
            self.THISTIMEAVERAGE = self.THISTIMEAVERAGE / self.test_times_avaliable
            self.TOTALTIMEAVERAGE = self.TOTALTIMEAVERAGE / self.test_times_avaliable
            self.WAITTIMEAVERAGE = self.WAITTIMEAVERAGE / self.test_times_avaliable
            self.ws.write(self.test_times_avaliable, 1, self.THISTIMEAVERAGE, self.style0)
            self.ws.write(self.test_times_avaliable, 3, self.TOTALTIMEAVERAGE, self.style0)
            self.ws.write(self.test_times_avaliable, 5, self.WAITTIMEAVERAGE, self.style0)

        self.wb.save(self.app_item[0] + '__' + Logout.FILE_NAME)

    def __loopOnce(self):
        '''start_calculator
            计算单次应用启动时间
        '''
        global DEBUG
        thisTime = ""
        totalTime = ""
        waitTime = ""
        thisTimeInteger = 0
        totalTimeInteger = 0
        waitTimeInteger = 0
        Logout.show_message('loopOnce')
        tempThisTime = self.THISTIMEAVERAGE
        tempTotalTime = self.TOTALTIMEAVERAGE
        tempWaitTime = self.WAITTIMEAVERAGE
        CommandExecuter.execute_command('adb shell svc power stayon true')
        (status, output) = CommandExecuter.execute_command('adb shell am start -W ' + self.app_item[1])
        parser = Parser(self.app_item[0], output, status)
        print("AppStartTime:output:" + output + "(end)");
        if (str(output).find("Status: ok") < 0):
            components = self.app_item[1].split("/");
            package = components[0];
            print("package:" + components[0]);
            (status, output) = CommandExecuter.execute_command('adb shell am start -W ' + package)
            parser = Parser(self.app_item[0], output, status)
            print("output:" + output + "(end)");
        try:
            Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, "Times: " + str(self.test_times_avaliable))
            Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, "Command result: " + str(status))
            Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, ''.join(output))
            Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, '---------------------------')
        except:
            Logout.show_message("log info failed")
            print(sys.exc_info()[0], sys.exc_info()[1])

        result = 0
        if parser.pre_parse() != -1:
            try:
                parser.parse();
                (thisTime, totalTime, waitTime) = parser.getParseResult()
                if DEBUG:
                    Logout.show_message('get_item_time...:' + thisTime + ", " + totalTime + ", " + waitTime)

                if thisTime.isdigit() and totalTime.isdigit() and waitTime.isdigit():
                    thisTimeInteger = int(thisTime)
                    totalTimeInteger = int(totalTime)
                    waitTimeInteger = int(waitTime)
                    if self.MAX_ITEM[0] <= thisTimeInteger:
                        self.MAX_ITEM[0] = thisTimeInteger

                    if self.MIN_ITEM[0] > thisTimeInteger:
                        self.MIN_ITEM[0] = thisTimeInteger

                    if self.MAX_ITEM[1] <= totalTimeInteger:
                        self.MAX_ITEM[1] = totalTimeInteger

                    if self.MIN_ITEM[1] > totalTimeInteger:
                        self.MIN_ITEM[1] = totalTimeInteger

                    if self.MAX_ITEM[2] <= waitTimeInteger:
                        self.MAX_ITEM[2] = waitTimeInteger

                    if self.MIN_ITEM[2] > waitTimeInteger:
                        self.MIN_ITEM[2] = waitTimeInteger

                    if DEBUG:
                        Logout.show_message('analyse command done')

                    Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE,
                                    "Write to excel: " + str(self.test_times_avaliable))

                    if thisTimeInteger == 0 or totalTime == 0 or waitTime == 0:
                        result = 0
                    else:
                        self.write_to_excel(self.ws, self.test_times_avaliable, thisTime, totalTime, waitTime)
                        self.THISTIMEAVERAGE += thisTimeInteger
                        self.TOTALTIMEAVERAGE += totalTimeInteger
                        self.WAITTIMEAVERAGE += waitTimeInteger
                        result = 1
            except:
                Logout.show_message('exception when start Activity: ' + self.app_item[1])

                print(sys.exc_info()[0], sys.exc_info()[1])

                Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, "Times: " + str(self.test_times_avaliable))
                Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, "Command result: " + str(status))
                Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, ''.join(output))
                Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, "parseResult(this,total,wait): " + \
                                 str(thisTime) + ", " + str(totalTime) + ", " + str(waitTime))
                Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, '---------------------------')
                self.THISTIMEAVERAGE = tempThisTime
                self.TOTALTIMEAVERAGE = tempTotalTime
                self.WAITTIMEAVERAGE = tempWaitTime
                result = 0
        try:
            mmresult = tencent_mm_exists()
            if mmresult == 0:
                Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, " tencent mm exists")
            else:
                self.tencent_mm_killed += 1
                Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE,
                                " tecent mm killed : " + str(self.tencent_mm_killed))

            qqresult = tencent_qq_exists()
            if qqresult == 0:
                Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE, " tencent qq exists")
            else:
                self.tencent_qq_killed += 1
                Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE,
                                " tencent qq killed : " + str(self.tencent_qq_killed))
        except:
            Logout.show_message('markt tencent_mm and tencent_qq failed')
            print(sys.exc_info()[0], sys.exc_info()[1])

        CommandExecuter.doubleBack()
        return result

    def __del__(self):
        Logout.show_message('......')


class GroupTest:

    def __init__(self):
        self.userInput = UserInput()
        self.overload = TestMode.getOverLoadMode()
        self.allTestApps = []

    def preLoop(self):
        overload = TestMode.getOverLoadMode()
        self.paths = OverLoad()
        if overload:
            self.paths.choose_overload_path()

        (self.apps, self.count) = self.userInput.input()

        APP_LIST = TestMode.getAllAppsList()
        APPS_INDEX = []

        if overload:
            overloadPath = self.paths.getOverLoadPath()
            for item in overloadPath:
                if item[3] not in APPS_INDEX:
                    APPS_INDEX.append(item[3])
                    item = TestItem(item, self.count, True)
                    self.allTestApps.append(item)

        for i in range(len(self.apps)):
            app_item = APP_LIST[int(self.apps[i])]
            if app_item[3] not in APPS_INDEX:
                APPS_INDEX.append(app_item[3])
                item = TestItem(APP_LIST[int(self.apps[i])], self.count, True)
                self.allTestApps.append(item)

    def __loopOnce(self):
        for testItem in self.allTestApps:
            testItem.test()

    def loopGroup(self):
        if self.overload:
            for i in range(self.count):
                self.__loopOnce()
        else:
            for testItem in self.allTestApps:
                for i in range(self.count):
                    testItem.test()


if __name__ == "__main__":
    '''__main__
        本程序用来统计应用启动时间，并求平均值
    '''
    Logout.show_message('I can calc app start time')
    TestMode.init()
    group = GroupTest()
    group.preLoop()
    group.loopGroup()
