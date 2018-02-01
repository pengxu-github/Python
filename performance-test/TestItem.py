#!/usr/bin/env python

from Logcat import Logout
import xlwt
from CommandExecuter import CommandExecuter
from Parser import Parser
import time
import TestMode

DEBUG = True


class TestItem:
    def __init__(self, app_item, testTime, record):
        self.record = record
        self.app_item = app_item
        self.testTime = testTime
        self.current_loop_times = 0
        self.test_times_avaliable = 0
        self.finished = False
        self.wb = xlwt.Workbook()
        self.style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
        self.ws = self.wb.add_sheet('Start Activity Time')

        self.THISTIMEAVERAGE = 0
        self.TOTALTIMEAVERAGE = 0
        self.WAITTIMEAVERAGE = 0
        self.overload = TestMode.getOverLoadMode()
        # [thisTime, totalTime, waitTime]
        self.MAX_ITEM = [0, 0, 0]
        self.MIN_ITEM = [100000000, 100000000, 100000000]
        self.execel_filename = self.app_item[0] + '__' + Logout.FILE_NAME

    def write_to_excel(self, ws, columes, thisTime, totalTime, waitTime):
        '''write_to_excel
            将测试结果缓存到 excel 表格中
        '''
        if DEBUG:
            Logout.show_message("saving pase result...　" + self.execel_filename)
        ws.write(columes, 0, "ThisTime")
        ws.write(columes, 1, int(thisTime))
        ws.write(columes, 2, "TotalTime")
        ws.write(columes, 3, int(totalTime))
        ws.write(columes, 4, "WaitTime")
        ws.write(columes, 5, int(waitTime))

    def test(self):
        Logout.show_message('Testing...' + self.app_item[0])

        if (self.current_loop_times < self.testTime):
            result = self.__loopOnce()
            Logout.show_message("测试次数： " + str(self.current_loop_times + 1))
            if result == 1:
                self.test_times_avaliable += 1
                Logout.show_message("有效测试次数： " + str(self.test_times_avaliable))
            self.current_loop_times += 1
            time.sleep(1)

        if self.current_loop_times >= self.testTime and self.finished == False:
            Logout.show_message("\n预设测试次数： " + str(self.testTime))
            Logout.show_message("有效测试次数： " + str(self.test_times_avaliable))

            Logout.show_message("\nthisTime max, min: " + str(self.MAX_ITEM[0]) + ", " + str(self.MIN_ITEM[0]))
            Logout.show_message("totalTime max, min: " + str(self.MAX_ITEM[1]) + ", " + str(self.MIN_ITEM[1]))
            Logout.show_message("waitTime max, min: " + str(self.MAX_ITEM[2]) + ", " + str(self.MIN_ITEM[2]))

            Logout.show_message("\nsum thisTime: " + str(self.THISTIMEAVERAGE))
            Logout.show_message("\nsum totalTime: " + str(self.TOTALTIMEAVERAGE))
            Logout.show_message("\nsum waitTime: " + str(self.WAITTIMEAVERAGE))
            if self.record:
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
                self.wb.save(self.execel_filename)
            self.finished = True

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
        tempThisTime = self.THISTIMEAVERAGE
        tempTotalTime = self.TOTALTIMEAVERAGE
        tempWaitTime = self.WAITTIMEAVERAGE
        CommandExecuter.execute_command('adb shell svc power stayon true')
        (status, output) = CommandExecuter.execute_command('adb shell am start -W ' + self.app_item[1])
        parser = Parser(self.app_item[0], output, status)
        print("TestItem:output:" + output + "(end)");
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
                    Logout.show_message('parse output result:' + thisTime + ", " + totalTime + ", " + waitTime)

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

                    Logout.log_temp(self.app_item[0] + '_' + Logout.OUTPUT_FILE,
                                    "Write to excel: " + str(self.test_times_avaliable))

                    if thisTimeInteger == 0 or totalTime == 0 or waitTime == 0:
                        result = 0
                    elif self.record:
                        self.write_to_excel(self.ws, self.test_times_avaliable, thisTime, totalTime, waitTime)
                        self.THISTIMEAVERAGE += thisTimeInteger
                        self.TOTALTIMEAVERAGE += totalTimeInteger
                        self.WAITTIMEAVERAGE += waitTimeInteger
                        result = 1
                    else:
                        result = 1
            except:
                Logout.show_message('exception when start Activity: ' + self.app_item[1])

                print(sys.exc_info()[0], sys.exc_info()[1])
                if self.record:
                    Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE,
                                     "Times: " + str(self.test_times_avaliable))
                    Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, "Command result: " + str(status))
                    Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, ''.join(output))
                    Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, "parseResult(this,total,wait): " + \
                                     str(thisTime) + ", " + str(totalTime) + ", " + str(waitTime))
                    Logout.log_error(self.app_item[0] + '_' + Logout.ERROR_FILE, '---------------------------')
                    self.THISTIMEAVERAGE = tempThisTime
                    self.TOTALTIMEAVERAGE = tempTotalTime
                    self.WAITTIMEAVERAGE = tempWaitTime
                result = 0
        if self.overload:
            CommandExecuter.pressHome()
        else:
            CommandExecuter.doubleBack()
        return result


if __name__ == "__main__":
    Logout.show_message('I am TestItem...')
