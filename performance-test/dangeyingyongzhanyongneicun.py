__author__ = 'wangshuancheng'
# from Tools.Scripts.treesync import raw_input
import subprocess
import xlwt


def execute_command(command):
    (status, ouput) = subprocess.getstatusoutput(command)
    return status, ouput


def findSegment(output, key):
    dataList = output.split()
    return dataList


def outputFilter(ws, msg, count):
    totalSegment = ''.join(msg)
    if totalSegment.find("TOTAL") != -1:

        # totalSegment = output_str.replace(" ","")
        totalSegment = totalSegment.strip('\n\n')
        totalSegment = totalSegment.splitlines()
        print('len = ' + str(len(totalSegment)))
        for i in range(len(totalSegment)):
            itemStr = totalSegment[i]
            if itemStr.find("TOTAL") != -1:
                resultArray = findSegment(itemStr, '')
                print("total = " + resultArray[1])
                ws.write(count, 0, "total")
                ws.write(count, 1, int(resultArray[1]))
                ws.write(count, 2, 'KB')
                break
            else:
                pass


def testMemoryInfo():
    initCount = 0
    guessStr = input('请输入数字：')
    wb = xlwt.Workbook()
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    ws = wb.add_sheet('Start Activity Time')
    if guessStr.isdigit():
        while True:
            guess = int(guessStr)
            if initCount < guess:
                (status, ouput) = execute_command('adb shell dumpsys meminfo com.freeme.calculator')
                outputFilter(ws, ouput, initCount)
            else:
                break
            initCount += 1
        else:
            print('输入错误，需要输入数字！')
    else:
        print('这个while循环结束')

    wb.save('com.freeme.calculator.xls')


testMemoryInfo()
print('Done')
